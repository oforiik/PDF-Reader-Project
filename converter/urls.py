from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload'),
    path('select/<uuid:file_id>/', views.select_pages, name='select_pages'),
    path('edit/<uuid:file_id>/', views.edit_text, name='edit_text'),
    path('generate/<uuid:file_id>/', views.generate_audio, name='generate_audio'),
    path('play/<uuid:audio_id>/', views.play_audio, name='play_audio'),
]