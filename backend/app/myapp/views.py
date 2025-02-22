# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404
from django.urls import reverse
from django.conf import settings
from urllib.parse import quote_plus, urlencode
import json

from .forms import PdfUploadForm
from .models import Pdf
# from .firebase_storage import upload_file  # Uncomment if needed for additional functionality
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_message(request):
    return Response({"message": "Hello, this is your message!"})

# def upload_pdf(request):
#     """
#     Handle PDF uploads via a form.
#     Renders a template with the upload form and saves the PDF upon submission.
#     """
#     if request.method == "POST":
#         form = PdfUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # The file is saved using GridFSStorage as defined in your model.
#             return HttpResponse("PDF uploaded successfully!")
#     else:
#         form = PdfUploadForm()
#     return render(request, 'upload_pdf.html', {'form': form})

# def view_pdf(request, pdf_id):
#     """
#     Retrieve and stream a PDF file.
#     Args:
#         pdf_id (int): The primary key of the Pdf model instance.
#     Returns:
#         A FileResponse streaming the PDF file.
#     Raises:
#         Http404 if the PDF does not exist.
#     """
#     pdf_instance = get_object_or_404(Pdf, id=pdf_id)
#     return FileResponse(pdf_instance.file, content_type='application/pdf')

# def delete_pdf(request, pdf_id):
#     """
#     Delete a PDF file.
#     Removes the file from the storage (GridFS) and deletes the associated model instance.
#     Args:
#         pdf_id (int): The primary key of the Pdf model instance.
#     Returns:
#         HttpResponse confirming deletion.
#     """
#     pdf_instance = get_object_or_404(Pdf, id=pdf_id)
#     pdf_instance.file.delete()  # Deletes the file from GridFSStorage.
#     pdf_instance.delete()       # Deletes the model instance from the database.
#     return HttpResponse("PDF deleted successfully!")

# # --- Auth0 Integration using Authlib ---

# from authlib.integrations.django_client import OAuth

# # Create an OAuth instance and register the Auth0 client
# oauth = OAuth()
# oauth.register(
#     "auth0",
#     client_id=settings.AUTH0_CLIENT_ID,
#     client_secret=settings.AUTH0_CLIENT_SECRET,
#     client_kwargs={"scope": "openid profile email"},
#     server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
# )

# def login(request):
#     """
#     Initiate the Auth0 login by redirecting the user to Auth0's authorize endpoint.
#     """
#     callback_url = request.build_absolute_uri(reverse("callback"))
#     return oauth.auth0.authorize_redirect(request, callback_url)

# def callback(request):
#     """
#     Handle the callback from Auth0.
#     Exchange the authorization code for tokens and store the token info in the session.
#     """
#     token = oauth.auth0.authorize_access_token(request)
#     request.session["user"] = token
#     # Redirect to the index page or another protected resource.
#     return redirect(request.build_absolute_uri(reverse("index")))

# def logout(request):
#     """
#     Log the user out locally and redirect to Auth0's logout endpoint.
#     """
#     request.session.clear()
#     params = {
#         "returnTo": request.build_absolute_uri(reverse("index")),
#         "client_id": settings.AUTH0_CLIENT_ID,
#     }
#     logout_url = f"https://{settings.AUTH0_DOMAIN}/v2/logout?" + urlencode(params, quote_via=quote_plus)
#     return redirect(logout_url)

# def index(request):
#     """
#     Render the home page showing session user data.
#     """
#     user = request.session.get("user")
#     return re
