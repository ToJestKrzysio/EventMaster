from django.views import generic

from event import models


class EventListView(generic.ListView):
    model = models.Event
    context_object_name = "events"
    template_name = "event/event_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        for event in context['events']:
            event.seats_left = 12

        return context
