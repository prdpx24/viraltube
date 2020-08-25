from django.utils import timezone
from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response

from .models import Video
from .serializers import VideoSerializer
from .queries import (
    get_video_queryset_by_query,
    get_video_queryset_by_title,
    get_video_queryset_by_description,
)
from .tasks import (
    run_periodic_background_task_and_update_db,
    fetch_and_save_youtube_videos_by_query_util,
)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.none()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = VideoSerializer

    def list(self, request):
        query = request.query_params.get("q")
        qs = get_video_queryset_by_query(query)
        if qs.exists() is False:
            # first fetch youtube videos via non-async util
            fetch_and_save_youtube_videos_by_query_util(query)
            qs = get_video_queryset_by_query(query)
        page = self.paginate_queryset(qs)
        serializer = VideoSerializer(page, many=True, context={"request": request})

        if query:
            # util to handle to periodic task, also it'll make sure to not create duplicate crons for same query
            run_periodic_background_task_and_update_db(query)

        return self.get_paginated_response(serializer.data)

    @decorators.action(
        detail=False, methods=["GET"], permission_classes=[permissions.AllowAny,]
    )
    def search(self, request):
        search_by_query = request.query_params.get("query")
        search_by_title = request.query_params.get("title")
        search_by_description = request.query_params.get("description")
        if search_by_query:
            qs = get_video_queryset_by_query(search_by_query)
        elif search_by_title:
            qs = get_video_queryset_by_title(search_by_title)
        else:
            qs = get_video_queryset_by_description(search_by_description)

        page = self.paginate_queryset(qs)
        serializer = VideoSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
