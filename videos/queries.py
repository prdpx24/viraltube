from django.core.cache import cache
from django.db.models import Q

from videos.models import APIKey, Video
from videos.constants import YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX, SECONDS_IN_A_DAY


def get_least_used_api_token_from_redis_store():
    prefix = YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX
    # redis-query
    keys = cache.keys(prefix + "*")
    api_key_hit_count_dict = cache.get_many(keys)
    if api_key_hit_count_dict:
        # get key for respective smallest number val in dict
        least_used_key = sorted(api_key_hit_count_dict, key=api_key_hit_count_dict.get)[
            0
        ]
        return least_used_key
    return None


def get_available_api_key_instance():
    # first check least used api_key in redis-store
    api_token = get_least_used_api_token_from_redis_store()
    if api_token:
        api_key_instance = APIKey.objects.filter(token=api_token).first()
        if api_key_instance and api_key_instance.is_quota_exhausted is False:
            return api_key_instance

    # On failure of above case,
    # get unused api_key from database, set it's hit_count to 0 in redis and start using it
    prefix = YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX
    keys = cache.keys(prefix + "*")
    api_key_yet_to_be_used_qs = APIKey.objects.exclude(token__in=keys)
    if api_key_yet_to_be_used_qs.exists():
        api_key = api_key_yet_to_be_used_qs.first()
        cache.set(
            YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX + api_key.token,
            0,
            timeout=SECONDS_IN_A_DAY,
        )
        return api_key

    # return None, when we actually ran out of all available api_key and their quota
    return None


def get_video_queryset_by_query(query):
    if query:
        title_query_chain = Q()
        description_query_chain = Q()
        for word in query.split(" "):
            title_query_chain = title_query_chain & Q(title__icontains=word)
            description_query_chain = description_query_chain & Q(
                description__icontains=word
            )
        return Video.objects.filter(
            title_query_chain | description_query_chain
        ).order_by("-published_at")
    return Video.objects.none()


def get_video_queryset_by_title(video_title):
    if video_title:
        query_chain = Q()
        for word in video_title.split(" "):
            query_chain = query_chain & Q(title__icontains=word)
        return Video.objects.filter(query_chain).order_by("-published_at")
    return Video.objects.none()


def get_video_queryset_by_description(description):
    if description:
        return Video.objects.filter(description__icontains=description).order_by(
            "-published_at"
        )
    return Video.objects.none()

