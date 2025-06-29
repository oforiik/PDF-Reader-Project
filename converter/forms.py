# converter/forms.py
from django import forms
from django.core.validators import FileExtensionValidator

class PdfUploadForm(forms.Form):
    pdf_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )