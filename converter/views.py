from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PDFDocument, ProcessedDocument
from .utils import generate_thumbnails, extract_pdf_text

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
    doc = get_object_or_404(PDFDocument, id=file_id, user=request.user)
    
    # Generate page thumbnails (first 24 pages)
    thumbnails = generate_thumbnails(doc.original_file.path)
    
    if request.method == 'POST':
        deleted_pages = request.POST.getlist('delete_pages')
        doc.pages_deleted = deleted_pages
        doc.save()
        return redirect('converter:edit_text', file_id=doc.id)
    
    return render(request, 'converter/page_select.html', {
        'doc': doc,
        'thumbnails': thumbnails
    })

@login_required
def edit_text(request, file_id):
    doc = get_object_or_404(PDFDocument, id=file_id, user=request.user)
    try:
        processed_doc = ProcessedDocument.objects.get(pdf=doc)
    except ProcessedDocument.DoesNotExist:
        # Create processed document if it doesn't exist
        processed_doc = ProcessedDocument.objects.create(
            pdf=doc,
            extracted_text=extract_pdf_text(doc.original_file.path)
        )
    
    if request.method == 'POST':
        edited_text = request.POST.get('edited_text', '')
        processed_doc.extracted_text = edited_text
        processed_doc.save()
        return redirect('converter:generate_audio', file_id=doc.id)
    
    return render(request, 'converter/edit_text.html', {
        'doc': doc,
        'text': processed_doc.extracted_text
    })

@login_required
def generate_audio(request, file_id):
    doc = get_object_or_404(PDFDocument, id=file_id, user=request.user)
    processed_doc = ProcessedDocument.objects.get(pdf=doc)
    
    if request.method == 'POST':
        # TODO: Implement audio generation logic here
        return redirect('converter:play_audio', audio_id=processed_doc.id)
    
    return render(request, 'converter/generate_audio.html', {
        'doc': doc
    })

@login_required
def play_audio(request, audio_id):
    processed_doc = get_object_or_404(ProcessedDocument, id=audio_id)
    
    return render(request, 'converter/play_audio.html', {
        'doc': processed_doc.pdf,
        'audio_url': processed_doc.audio_file.url if processed_doc.audio_file else None
    })