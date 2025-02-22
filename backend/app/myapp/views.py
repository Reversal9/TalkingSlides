# views.py

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

@api_view(['GET'])
def get_message(request):
    """
    A simple API endpoint to test the service.
    Returns:
        JSON response with a test message.
    """
    return Response({"message": "Hello, this is your message!"}, status=status.HTTP_200_OK)

def upload_pdf(request):
    """
    View to handle PDF uploads via a form.
    Renders a template with the upload form and saves the PDF upon submission.
    """
    if request.method == "POST":
        form = PdfUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # The file is saved using GridFSStorage as defined in your model.
            return HttpResponse("PDF uploaded successfully!")
    else:
        form = PdfUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

def view_pdf(request, pdf_id):
    """
    View to retrieve and stream a PDF file.
    Args:
        pdf_id: The primary key of the Pdf model instance.
    Returns:
        FileResponse streaming the PDF file with appropriate content type.
    Raises:
        Http404 if the PDF does not exist.
    """
    pdf_instance = get_object_or_404(Pdf, id=pdf_id)
    return FileResponse(pdf_instance.file, content_type='application/pdf')

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

def upload_video(request):
    """
    View to handle video uploads via a form.
    Renders a template with the upload form and saves the video upon submission.
    """
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # The file is saved using GridFSStorage as defined in your model.
            return HttpResponse("video uploaded successfully!")
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

def view_video(request, video_id):
    """
    View to retrieve and stream a video file.
    Args:
        video_id: The primary key of the video model instance.
    Returns:
        FileResponse streaming the video file with appropriate content type.
    Raises:
        Http404 if the video does not exist.
    """
    video_instance = get_object_or_404(VideoMetadata, id=video_id)
    return FileResponse(video_instance.file, content_type='application/video')

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

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def index(request):

    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


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

client = MongoClient("mongodb://localhost:27017/")
db = client["videosDB"]
fs = gridfs.GridFS(db)

THUMBNAIL_DIR = "media/thumbnails/"

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
            filename=video_file.name,
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
def get_video(request, filename):
    file = fs.find_one({"filename": filename})
    if not file:
        return JsonResponse({"error": "File not found"}, status=404)

    response = StreamingHttpResponse(file, content_type="video/mp4")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
