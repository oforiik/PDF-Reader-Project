import uuid
from django.db import models
from django.contrib.auth.models import User

class PDFDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    pages_deleted = models.JSONField(default=list)  # Store deleted page indexes

class ProcessedDocument(models.Model):
    pdf = models.OneToOneField(PDFDocument, on_delete=models.CASCADE)
    extracted_text = models.TextField()
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)