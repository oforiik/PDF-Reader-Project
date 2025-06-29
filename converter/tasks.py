from celery import shared_task
from gtts import gTTS
from django.conf import settings
import os

@shared_task
def generate_audio_task(text, output_path):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        return True
    except Exception as e:
        # Log error
        return False