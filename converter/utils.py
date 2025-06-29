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
