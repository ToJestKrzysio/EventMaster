from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.utils import timezone


def now_with_delay():
    return timezone.now() + timedelta(weeks=1)


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING,
                               editable=False, blank=True, null=False)
    publish_date = models.DateField(default=timezone.now)
    hide_date = models.DateField(default=now_with_delay)
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
