from django.db import models
from django.core.cache import cache


from .constants import YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX


class Video(models.Model):
    title = models.CharField(max_length=1000, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    youtube_video_id = models.CharField(max_length=100, blank=False, null=False)

    channel_name = models.CharField(max_length=500, blank=False, null=False)

    thumbnail_url = models.URLField()

    published_at = models.DateTimeField(blank=False, null=False)

    class Meta:
        indexes = [
            models.Index(fields=["title", "youtube_video_id"]),
        ]

    @staticmethod
    def get_video_id_from_youtube_video_url(video_url):
        return video_url.replace("https://www.youtube.com/watch?v=", "")

    @property
    def youtube_url(self):
        return "https://www.youtube.com/watch?v={}".format(self.youtube_video_id)

    def __str__(self):
        return "{title} - {channel_name}".format(
            title=self.title, channel_name=self.channel_name
        )


class APIKey(models.Model):
    name = models.CharField(
        max_length=255, blank=False, null=False, default="Youtube API"
    )
    token = models.CharField(max_length=255, blank=False, null=False)
    query_limit_per_day = models.PositiveIntegerField(
        blank=False, null=False, default=10000
    )

    @property
    def remaining_queries(self):
        # cache_key = youtube_api_hit_count
        key = YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX + self.token
        if key in cache:
            return cache.get(key) - self.query_limit_per_day
        return self.query_limit_per_day

    @property
    def is_quota_exhausted(self):
        return True if self.remaining_queries <= 0 else False

    def __str__(self):
        return "{token}".format(token=self.token)
