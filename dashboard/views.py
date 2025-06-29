from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def file_manager(request):
    # Will show user's previous conversions
    return render(request, 'dashboard/file_manager.html')