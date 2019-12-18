from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse


class Photo(models.Model):

    DRAFT = "draft"
    PUBLISHED = "published"

    STATUSES = (
        (DRAFT, "this photo is draft"),
        (PUBLISHED, "this photo is published"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=10, choices=STATUSES)
    content = models.ImageField(upload_to="user_photos/")
    counter_views = models.PositiveIntegerField(default=0)

    def has_been_liked_by_user(self, user):
        return self.photolikes_set.filter(user=user).exists()

    def get_absolute_url(self):
        return reverse("detail_photo", kwargs={"pk": self.pk})

    def likes_count(self):
        return self.photolikes_set.count()

    def __str__(self):
        return self.title

class PhotoLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)