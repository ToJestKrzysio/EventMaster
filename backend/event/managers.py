from django.db import models
from django.db.models import Count, Q
from django.db.models.functions import Now


class EventRegistrationCountManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            seats_taken=Count(
                "registration__event_id",
                filter=(Q(registration__payment_completed=True) |
                        Q(registration__payment_deadline__gt=Now()))
            )
        )
