from django.contrib import admin

from .models import Video, APIKey


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "channel_name")
    search_fields = ["title", "description", "channel_name", "youtube_video_id"]


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "token",
    )
    search_fields = ("token",)
