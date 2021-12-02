from django.views import generic

from event import models


class EventListView(generic.ListView):
    model = models.Event
    context_object_name = "events"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        for event in context['events']:
            event.seats_left = max(
                0, event.max_occupancy - event.current_occupancy)
        return context
