from django.db import models

from django.contrib.auth.models import User


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

    def __str__(self):
        return self.title