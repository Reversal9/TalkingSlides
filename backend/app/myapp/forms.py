# forms.py
from django import forms
from .models import Pdf

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ['file']
