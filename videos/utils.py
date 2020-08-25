import requests

from django.core.cache import cache
from django.utils.dateparse import parse_datetime

from videos.constants import YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX, SECONDS_IN_A_DAY


class YoutubeAPIClient:
    """
    A simple youtube api client
    """

    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, api_token):
        self.api_token = api_token
        self.query_params = {
            "part": "snippet",
            "key": self.api_token,
            "q": None,
            "type": "video",
            "order": "date",
            "maxResults": 10,
            "nextPageToken": None,
        }

    def prepare_request(self):
        params = ""
        for key, val in self.query_params.items():
            if val:
                params += "{key}={val}&".format(key=key, val=val)

        request_url = self.SEARCH_URL + "?{params}".format(params=params)
        return request_url

    @staticmethod
    def increment_api_hit_count(api_token):
        key = YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX + api_token
        if key not in cache:
            cache.set(key, 1, timeout=SECONDS_IN_A_DAY)
        else:
            cache.incr(key)

    @staticmethod
    def set_quota_exceeded_on_api_token(api_token):
        key = YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX + api_token
        if key not in cache:
            cache.set(key, 10000, timeout=SECONDS_IN_A_DAY)
        else:
            cache.set(key, 10000, timeout=SECONDS_IN_A_DAY)

    def search(self, q, next_page_token=None, order_by="date", page_size=10):
        self.query_params["q"] = q
        self.query_params["nextPageToken"] = next_page_token
        self.query_params["order"] = order_by
        self.query_params["maxResults"] = page_size
        url = self.prepare_request()
        resp = requests.get(url)

        if resp.status_code == 200:
            YoutubeAPIClient.increment_api_hit_count(self.api_token)
            return resp.json()
        else:
            print("API Error")
            print(resp.json()["error"]["message"])
            YoutubeAPIClient.set_quota_exceeded_on_api_token(self.api_token)

        # else fail silently
        return None

    def serialize_response(self, response):
        items = response.get("items", [])
        result = []
        for item in items:
            data = {
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "youtube_video_id": item["id"]["videoId"],
                "channel_name": item["snippet"]["channelTitle"],
                "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"],
                "published_at": parse_datetime(item["snippet"]["publishTime"]),
            }
            result.append(data)
        return result

