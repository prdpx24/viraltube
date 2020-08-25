from django.conf.urls import url, include
from . import views

from rest_framework import routers

from .viewsets import VideoViewSet

app_name = "videos"

router = routers.SimpleRouter()
router.register("videos", VideoViewSet, basename="videos")

urlpatterns = [
    url(r"^api/", include(router.urls)),
]
