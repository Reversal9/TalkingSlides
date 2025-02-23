from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404, JsonResponse, StreamingHttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import PdfUploadForm, VideoUploadForm
from .models import Pdf, VideoMetadata
import gridfs
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import ffmpeg
# from .firebase_storage import upload_file  # Uncomment if needed for additional functionality
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import os
from bson import ObjectId
import openai
# from pdfminer.high_level import extract_text
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from dotenv import load_dotenv
import base64
from django.conf import settings  # ✅ Import settings
import openai
from openai import OpenAIError, AuthenticationError, RateLimitError  # ✅ Correct import
from django.core.cache import cache

# ✅ Set OpenAI API Key from Django settings
openai.api_key = settings.OPENAI_API_KEY  # ✅ Correct way to access it



@api_view(['GET'])
def get_message(request):
    """
    A simple API endpoint to test the service.
    Returns:
        JSON response with a test message.
    """
    return Response({"message": "Hello, this is your message!"}, status=status.HTTP_200_OK)

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    api_base_url="http://localhost:5173/",
    access_token_url="http://localhost:5173/oauth/token",
    authorize_url="http://localhost:5173/authorize",
    client_kwargs={"scope": "openid profile email"},
)

def index(request):
    return redirect("http://localhost:5173/")

def callback(request):
    try:
        token = oauth.auth0.authorize_access_token(request)
        user_info = oauth.auth0.parse_id_token(request, token)
        request.session["user"] = user_info
        return redirect("http://localhost:5173/dashboard")  # Redirect to React frontend
    except Exception as e:
        print("Auth0 callback error:", str(e))
        return redirect("/") 
    
def login(request):
    return oauth.auth0.authorize_redirect(request, request.build_absolute_uri("/callback"))

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

THUMBNAIL_DIR = "media/thumbnails/"

client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
db = client[settings.DATABASES['default']['NAME']]
fs = gridfs.GridFS(db)  # Initialize GridFS

@csrf_exempt
def upload_video(request):
    if request.method == "POST" and request.FILES.get("video"):
        video_file = request.FILES["video"]
        video_id = fs.put(video_file, filename=video_file.name)

        # Generate thumbnail
        video_path = f"/tmp/{video_file.name}"
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{video_file.name}.jpg")

        with open(video_path, "wb") as f:
            f.write(video_file.read())

        generate_thumbnail(video_path, thumbnail_path)

        # Save metadata
        video_metadata = VideoMetadata.objects.create(
            file=video_file,
            file_id=video_id,
            title=video_file.name,
            thumbnail=thumbnail_path.replace("media/", "")
        )

        return JsonResponse({"message": "Video uploaded", "video_id": str(video_id)})

    return JsonResponse({"error": "Invalid request"}, status=400)

def generate_thumbnail(video_path, thumbnail_path):
    try:
        (
            ffmpeg
            .input(video_path, ss=1)  # Capture frame at 1 second
            .output(thumbnail_path, vframes=1)
            .run(overwrite_output=True)
        )
    except Exception as e:
        print("Error generating thumbnail:", e)

@csrf_exempt
def get_video(request, file_id):
    try:
        # Convert the file_id to ObjectId
        file_id = ObjectId(file_id)
    except Exception as e:
        return JsonResponse({"error": "Invalid file ID"}, status=400)

    # Retrieve the file from GridFS
    file = fs.find_one({"_id": file_id})
    
    if not file:
        return JsonResponse({"error": "File not found"}, status=404)

    # Create a generator to stream the video file
    def file_iterator():
        # Fetch the video data in chunks
        chunk_size = 1024 * 1024  # 1 MB chunks
        with file as video_file:
            while True:
                chunk = video_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    # Set the appropriate content type for video streaming
    response = StreamingHttpResponse(file_iterator(), content_type="video/mp4")
    
    # Set the content-disposition header for inline viewing or download
    response['Content-Disposition'] = f'inline; filename="{file.filename}"'
    
    return response

def list_videos(request):
    cached_data = cache.get("video_list")
    if cached_data:
        return JsonResponse(cached_data, safe=False)

    videos = VideoMetadata.objects.all()
    data = [
        {
            "title": video.title,
            "file_id": video.file_id,
            "thumbnail": video.thumbnail.url if video.thumbnail else None
        }
        for video in videos
    ]

    cache.set("video_list", data, timeout=60)  # ✅ Cache for 60 seconds
    return JsonResponse(data, safe=False)

@csrf_exempt
def upload_pdf(request):
    """
    View to handle PDF uploads via a form.
    Renders a template with the upload form and saves the PDF upon submission.
    """
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf_file = request.FILES["pdf"]
        
        # Save the PDF file to GridFS and retrieve the file_id
        file_id = fs.put(pdf_file, filename=pdf_file.name)

        # Save the file_id into the Pdf model
        pdf = Pdf.objects.create(
            file=pdf_file,
            file_id=file_id,
        )

        return JsonResponse({"message": "Pdf uploaded", "file_id": str(file_id)})

    return JsonResponse({"error": "Invalid request"}, status=400)
    # if request.method == "POST":
    #     form = PdfUploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()  # The file is saved using GridFSStorage as defined in your model.
    #         return HttpResponse("PDF uploaded successfully!")
    # else:
    #     form = PdfUploadForm()
    # return render(request, 'upload_pdf.html', {'form': form})

def view_pdf(request, file_id):
    """
    View to retrieve and stream a PDF file from GridFS.
    Args:
        file_id: The ObjectId (string) of the Pdf model instance.
    Returns:
        StreamingHttpResponse streaming the PDF file with appropriate content type.
    """
    try:
        # Convert file_id string to ObjectId
        file_id = ObjectId(file_id)
    except Exception:
        return JsonResponse({"error": "Invalid file ID"}, status=400)

    # Retrieve the file from GridFS
    file = fs.find_one({"_id": file_id})

    if not file:
        return JsonResponse({"error": "File not found"}, status=404)

    # Create a generator function to stream the file in chunks
    def file_iterator():
        chunk_size = 8192  # 8 KB chunks
        with file as pdf_file:
            while True:
                chunk = pdf_file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    # Use StreamingHttpResponse for large file handling
    response = StreamingHttpResponse(file_iterator(), content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{file.filename}"'

    return response

def delete_pdf(request, pdf_id):
    """
    View to delete a PDF file.
    Removes the file from the storage (GridFS) and deletes the associated model instance.
    Args:
        pdf_id: The primary key of the Pdf model instance.
    Returns:
        HttpResponse confirming deletion.
    """
    pdf_instance = get_object_or_404(Pdf, id=pdf_id)
    pdf_instance.file.delete()  # Deletes the file from GridFSStorage.
    pdf_instance.delete()       # Deletes the model instance from the database.
    return HttpResponse("PDF deleted successfully!")

def delete_video(request, video_id):
    """
    View to delete a video file.
    Removes the file from the storage (GridFS) and deletes the associated model instance.
    Args:
        video_id: The primary key of the video model instance.
    Returns:
        HttpResponse confirming deletion.
    """
    video_instance = get_object_or_404(VideoMetadata, id=video_id)
    video_instance.file.delete()  # Deletes the file from GridFSStorage.
    video_instance.delete()       # Deletes the model instance from the database.
    return HttpResponse("video deleted successfully!")

def webhook_handler(request):
    if (request.method != "POST"): 
        return Response({"message": "Webhook received successfully"}, status=status.HTTP_200_OK)
    payload = json.loads(request.body)
    event = payload.get("event")
    
    if (event == "SUCCESS"):
        return Response({"message" : "processing completed successfully."})
    else:
        return Response({"message": "processing failed."})

'''
@app.post("/compile_video/")
async def compile_video_endpoint(
    pdf_file: UploadFile = File(...), 
    speech_path: str = Form(...),
    vid_path: str = Form(...),
    webhook_url: str = Form(...),
    background_tasks: BackgroundTasks
):
    try:
        # Save the uploaded PDF file temporarily
        pdf_filename = os.path.join(TEMP_DIR, pdf_file.filename)
        with open(pdf_filename, "wb") as f:
            shutil.copyfileobj(pdf_file.file, f)

        # Run the video compilation in the background
        background_tasks.add_task(compile_video, pdf_filename, speech_path, vid_path, webhook_url)

        return JSONResponse({"message": "Video compilation started successfully. You will be notified when it's done."}, status_code=200)
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
'''

openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def text_to_speech(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get("text", "")

            if not text:
                return JsonResponse({"error": "No text provided"}, status=400)

            if not openai.api_key:
                return JsonResponse({"error": "OpenAI API key is missing"}, status=500)

            # ✅ Correct OpenAI API Call
            response = openai.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )

            # ✅ Ensure response contains data
            audio_data = response.get("data")

            if not audio_data:
                return JsonResponse({"error": "Invalid response from OpenAI"}, status=500)

            # ✅ Encode audio as base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            return JsonResponse({"audio": audio_base64})

        except AuthenticationError:
            return JsonResponse({"error": "Invalid OpenAI API Key"}, status=401)
        except RateLimitError:
            return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)
        except OpenAIError as e:
            return JsonResponse({"error": f"OpenAI API error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
