from django.shortcuts import render

from photos.models import Photo

def index(request):
    photo_list = Photo.objects.filter(status=Photo.PUBLISHED)
    return render(request, 'photos/index.html', {"photo_list" : photo_list})
