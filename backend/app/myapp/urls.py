from django.contrib import admin
from django.urls import path
from .views import get_message, upload_pdf, view_pdf, delete_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('message/', get_message, name='get_message'),
    path('upload/', upload_pdf, name='upload_pdf'),
    path('view/<int:pdf_id>/', view_pdf, name='view_pdf'),
    path('delete/<int:pdf_id>/', delete_pdf, name='delete_pdf'),
]
