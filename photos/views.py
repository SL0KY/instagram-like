from django.shortcuts import render
from django.urls import reverse_lazy
from photos.models import Photo
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

def index(request):
    photo_list = Photo.objects.filter(status=Photo.PUBLISHED)
    return render(request, 'photos/index.html', {"photo_list" : photo_list})

class PhotoCreateView(SuccessMessageMixin, CreateView):
    model = Photo
    fields = ["title", "description", "status", "content", "user"]
    template_name = "photos/upload.html"
    success_url = reverse_lazy("list_photos")
    success_message = "%(title)s à été ajoutée avec succès"

    def get_initial(self):
        return {"user" : self.request.user}

