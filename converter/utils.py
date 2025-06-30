import os
from PIL import Image
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

def generate_thumbnails(pdf_path):
    """
    Generate thumbnails from a PDF file.
    Returns a list of thumbnail image paths.
    """
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        thumbnails = []
        
        # Save thumbnails
        for i, image in enumerate(images):
            thumbnail_path = f"thumbnails/{os.path.basename(pdf_path)}_page_{i+1}.jpg"
            image.save(thumbnail_path, 'JPEG')
            thumbnails.append(thumbnail_path)
        
        return thumbnails
    except Exception as e:
        print(f"Error generating thumbnails: {e}")
        return []

def generate_page_thumbnails(pdf_path, output_dir, max_pages=24):
    images = convert_from_path(pdf_path, dpi=70, first_page=1, last_page=max_pages)
    
    for i, image in enumerate(images):
        # Create thumbnail
        image.thumbnail((200, 300))
        thumb_path = os.path.join(output_dir, f"page_{i+1}.jpg")
        image.save(thumb_path, "JPEG")
    
    return len(images)

def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF file.
    Returns the extracted text as a string.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text()
        
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
