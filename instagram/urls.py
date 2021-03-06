"""insta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework import routers

from photos.api import views as photo_api_views
from photos import views as photo_views

router = routers.DefaultRouter()
router.register(r'photos', photo_api_views.PhotoViewSet)

urlpatterns = [
    path('api/v1', include(router.urls)),
    path('^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("", photo_views.index),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('photos/', photo_views.index, name="list_photos"),
    path("photos/create", photo_views.PhotoCreateView.as_view(), name='create_photo'),
    path("photos/like", photo_views.PhotoLikeView.as_view(), name="like_photo"),
    path("photos/<int:pk>", photo_views.PhotoDetailView.as_view(), name="detail_photo"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
