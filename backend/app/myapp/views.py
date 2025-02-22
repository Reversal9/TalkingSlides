# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import PdfUploadForm
from .models import Pdf
# from .firebase_storage import upload_file  # Uncomment if needed for additional functionality
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

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
    return Response({"message": "Hello, this is your message!"})

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
