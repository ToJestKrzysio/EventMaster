from django.contrib.auth import get_user_model
from django.db import models

from event.helpers import user_event_deadline
from event.managers import EventRegistrationCountManager


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_occupancy = models.IntegerField()
    location = models.CharField(max_length=50)

    creator = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING,
                                editable=False)
    creation_date = models.DateTimeField(auto_now=True, editable=False)

    # Custom managers
    objects = models.Manager()
    objects_with_registrations = EventRegistrationCountManager()

    def __str__(self):
        return f"{self.title}"


class Registration(models.Model):
    event = models.ForeignKey("Event", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    payment_completed = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_deadline = models.DateTimeField(default=user_event_deadline)
    created = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, null=True,
                                    editable=False, related_name='modified_by')

    def __str__(self):
        return f"{self.event.title} - {self.user}"
