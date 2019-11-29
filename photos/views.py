from django.shortcuts import render
from django.urls import reverse_lazy
from photos.models import Photo, PhotoLikes
from django.views.generic.edit import CreateView, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse

def index(request):
    photo_list = Photo.objects.filter(status=Photo.PUBLISHED)
    #if request.user.is_authenticated:
     #   user = request.user
      #  photo_likes = PhotoLikes.objects.filter(user=user)
       # for i in range photo_list.all():
        #    for j in range photo_likes.count():
         #       if photo_list[i].photo_id = photo_likes[j].photo_id:
          #          photo_list[i].is_liked = True 


    return render(request, 'photos/index.html', {"photo_list" : photo_list})

class PhotoCreateView(SuccessMessageMixin, CreateView):
    model = Photo
    fields = ["title", "description", "status", "content", "user"]
    template_name = "photos/upload.html"
    success_url = reverse_lazy("list_photos")
    success_message = "%(title)s à été ajoutée avec succès"

    def get_initial(self):
        return {"user" : self.request.user}

class PhotoLikeView(SuccessMessageMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            photo_id = request.POST.get("photo_id")
            user = request.user

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
        else:
            status = "user not auth"

        return HttpResponse(f"{photo_id} was {status}")