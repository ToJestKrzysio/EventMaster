from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    start_time = models.DateTimeField()
    duration = models.DurationField(default="00:05:00")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_occupancy = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    location = models.CharField(max_length=50)

    creator = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING,
                                editable=False)
    creation_date = models.DateTimeField(auto_now=True, editable=False)


def user_event_deadline():
    return timezone.now() + timedelta(weeks=1)


class Registration(models.Model):
    event = models.ForeignKey("Event", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    payment_completed = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_deadline = models.DateTimeField(default=user_event_deadline)

    def __str__(self):
        return f"{self.event} - {self.user}"
