# File to manage constants values to be used in throughout the project


SECONDS_IN_A_DAY = 24 * 60 * 60

# We will keep api hit count in redis in KEY:VAL pair,
# i.e. youtube_api_hit_count-API_KEY : HIT_COUNT
YOUTUBE_API_HIT_COUNT_CACHE_KEY_PREFIX = "youtube_api_hit_count-"

SEARCH_QUERY_KEY = "youtube-search-query"
