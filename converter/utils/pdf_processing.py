import os
from pdf2image import convert_from_path
from PIL import Image
from django.conf import settings

def generate_page_thumbnails(pdf_path, output_dir, max_pages=24):
    os.makedirs(output_dir, exist_ok=True)
    thumbnails = []
    
    images = convert_from_path(pdf_path, dpi=50, first_page=1, last_page=max_pages)
    
    for i, image in enumerate(images):
        # Resize to thumbnail
        image.thumbnail((200, 300))
        thumb_path = os.path.join(output_dir, f"page_{i+1}.jpg")
        image.save(thumb_path, "JPEG")
        thumbnails.append(thumb_path)
    
    return thumbnails