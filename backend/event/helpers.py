from datetime import timedelta

from django.utils import timezone


def user_event_deadline():
    return timezone.now() + timedelta(weeks=1)
