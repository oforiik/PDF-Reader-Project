from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PDFDocument, ProcessedDocument
from .utils import generate_page_thumbnails, extract_pdf_text
import json
import os
from django.conf import settings
from .tasks import generate_audio_task

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']
        doc = PDFDocument.objects.create(
            user=request.user,
            original_file=pdf_file
        )
        return redirect('converter:select_pages', file_id=doc.id)
    return render(request, 'converter/upload.html')

@login_required
def select_pages(request, file_id):
    document = get_object_or_404(PdfDocument, id=file_id, user=request.user)
    
    # Create thumbnail directory path
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails', str(document.id))
    
    # Generate thumbnails if they don't exist
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir, exist_ok=True)
        generate_page_thumbnails(document.file.path, thumbnail_dir)
    
    # Get list of generated thumbnails
    thumbnails = [f for f in os.listdir(thumbnail_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Process form submission
    if request.method == 'POST':
        deleted_pages = request.POST.getlist('delete_pages')
        document.deleted_pages = json.dumps(deleted_pages)
        document.save()
        return redirect('edit_text', file_id=document.id)
    
    return render(request, 'converter/page_selection.html', {
        'document': document,
        'thumbnails': thumbnails,
        'thumbnail_url': os.path.join(settings.MEDIA_URL, 'thumbnails', str(document.id))
    })

@login_required
def edit_text(request, file_id):
    document = get_object_or_404(PdfDocument, id=file_id, user=request.user)
    
    # Extract text excluding deleted pages
    deleted_pages = json.loads(document.deleted_pages) if document.deleted_pages else []
    text = extract_pdf_text(document.file.path, excluded_pages=deleted_pages)
    
    if request.method == 'POST':
        edited_text = request.POST.get('text_content', '')
        # Save edited text to database or session
        request.session['edited_text'] = edited_text
        return redirect('generate_audio', file_id=document.id)
    
    return render(request, 'converter/edit_text.html', {
        'document': document,
        'initial_text': text
    })
    
@login_required
def generate_audio(request, file_id):
    document = get_object_or_404(PdfDocument, id=file_id, user=request.user)
    
    # Get edited text from session
    text = request.session.get('edited_text', '')
    
    # Generate unique filename
    audio_filename = f"audio_{document.id}_{int(time.time())}.mp3"
    audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', audio_filename)
    
    # Start background task
    generate_audio_task.delay(text, audio_path)
    
    # Create audio object
    audio_file = AudioFile.objects.create(
        document=document,
        audio_file=os.path.join('audio', audio_filename),
        status='PROCESSING'
    )
    
    return render(request, 'converter/processing.html', {
        'document': document,
        'audio_file': audio_file
    })

@login_required
def play_audio(request, audio_id):
    processed_doc = get_object_or_404(ProcessedDocument, id=audio_id)
    
    return render(request, 'converter/play_audio.html', {
        'doc': processed_doc.pdf,
        'audio_url': processed_doc.audio_file.url if processed_doc.audio_file else None
    })