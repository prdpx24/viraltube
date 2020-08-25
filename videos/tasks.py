import os
import json

from django.utils import timezone
from django.conf import settings

from django_celery_beat.models import PeriodicTask, CrontabSchedule


from tasks import app, is_broker_available
from .queries import get_available_api_key_instance
from .models import Video
from .serializers import VideoSerializer
from .utils import YoutubeAPIClient


def run_periodic_background_task_and_update_db(query):
    if is_broker_available():
        # check if background task already exists for query
        if PeriodicTask.objects.filter(kwargs__icontains=query).exists():
            # do nothing
            pass
        else:
            bg_cron_conf = settings.BACKGROUND_TASK_CRONTAB_SCHEDULE
            crontab, _ = CrontabSchedule.objects.get_or_create(**bg_cron_conf)
            PeriodicTask.objects.create(
                crontab=crontab,
                name="async_fetch_youtube_videos_by_query:{}".format(query),
                task="videos.tasks.async_fetch_youtube_videos_by_query",
                args=json.dumps([]),
                kwargs=json.dumps({"query": query}),
            )


def fetch_and_save_youtube_videos_by_query_util(query):
    api_key = get_available_api_key_instance()
    if api_key:
        yt_client = YoutubeAPIClient(api_key.token)
        resp = yt_client.search(query, order_by="date", page_size=50)
        if resp:
            serialized_resp = yt_client.serialize_response(resp)

            video_instances_to_create = []
            for video_item in serialized_resp:
                if (
                    Video.objects.filter(
                        youtube_video_id=video_item["youtube_video_id"]
                    ).exists()
                    is False
                ):
                    video_instances_to_create.append(Video(**video_item))

            if video_instances_to_create:
                # bulk_create for faster performance
                Video.objects.bulk_create(video_instances_to_create)


@app.task(bind=True)
def async_fetch_youtube_videos_by_query(*args, **kwargs):
    query = kwargs.get("query")
    if query:
        print("calling util func to fetch and save only new videos")
        fetch_and_save_youtube_videos_by_query_util(query)


@app.task(bind=True)
def test_task(*args, **kwargs):
    print("executing test_task with args", args, "& kwargs", kwargs)

