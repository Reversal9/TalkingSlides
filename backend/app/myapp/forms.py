# forms.py
from django import forms
from .models import Pdf, Video

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ['file']

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file']
