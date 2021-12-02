from django.db.models import Count, Case, When, Q, F, Value
from django.db.models.functions import Now
from django.views import generic

from event.models import Event


class EventListView(generic.ListView):
    model = Event
    context_object_name = "events"
    template_name = "event/event_list.html"

    def get_queryset(self):
        queryset = Event.objects.annotate(
            seats_taken=Count(
                "registration__event_id",
                filter=(Q(registration__payment_completed=True) |
                        Q(registration__payment_deadline__lt=Now()))
            )
        )
        return queryset
