import os

from django.utils import timezone
from django.conf import settings


from tasks import app, is_broker_available


def run_periodic_background_task_and_update_db(query):
    if is_broker_available():
        pass
