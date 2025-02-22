from django.contrib import admin
from django.urls import path
from .views import get_message, upload_pdf, view_pdf, delete_pdf, index, upload_video, list_videos, get_video
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('message/', get_message, name='get_message'),
    path('upload-pdf/', upload_pdf, name='upload_pdf'),
    path('view-pdf/<int:pdf_id>/', view_pdf, name='view_pdf'),
    path('delete-pdf/<int:pdf_id>/', delete_pdf, name='delete_pdf'),
    path('message/', views.get_message, name='get_message'),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path('', index, name='index'),
    path("api/upload/", views.upload_video, name="upload_video"),
    path("api/video/<str:file_id>/", views.get_video, name="get_video"),
    path("api/videos/", views.list_videos, name="list_videos"),
]
