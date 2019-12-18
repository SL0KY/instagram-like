from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from photos.models import Photo, PhotoLikes
from django.views.generic.edit import CreateView, View
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.db.models import Count, Q

def index(request):
    photo_list = Photo.objects.filter(status=Photo.PUBLISHED).annotate(
        likes_count=Count("photolikes", filter=Q(photolikes__user=request.user))
    ).select_related("user")

    return render(request, 'photos/index.html', {"photo_list" : photo_list})

class PhotoCreateView(SuccessMessageMixin, CreateView):
    model = Photo
    fields = ["title", "description", "status", "content", "user"]
    template_name = "photos/upload.html"
    success_url = reverse_lazy("list_photos")
    success_message = "%(title)s à été ajoutée avec succès"

    def get_initial(self):
        return {"user" : self.request.user}

class PhotoDetailView(DetailView):
    model = Photo
    template_name = "photos/photo_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["liked"] = self.object.has_been_liked_by_user(self.request.user) 
        return context
    
class PhotoLikeView(LoginRequiredMixin, View):
    success_url = reverse_lazy("list_photos")

    def post(self, request, *args, **kwargs):
        photo_id = request.POST.get("photo_id")
        user = request.user
        photo = get_object_or_404(Photo, pk=photo_id)

        photo_like = PhotoLikes.objects.filter(
            photo_id=photo_id,
            user=user
        )

        if photo_like.exists():
            photo_like.delete()
            status = "unliked"
        else:
            PhotoLikes.objects.create(
                photo_id=photo_id,
                user=user,
            )
            status = "liked"
        
        messages.success(self.request, f"{photo_id} was {status}")

        return redirect(photo.get_absolute_url())