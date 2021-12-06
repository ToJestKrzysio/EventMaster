from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.db.models.functions import Now
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from event.models import Event, Registration


class EventListView(generic.ListView):
    model = Event
    context_object_name = "events"
    template_name = "event/event_list.html"

    def get_queryset(self):
        queryset = Event.objects.annotate(
            seats_taken=Count(
                "registration__event_id",
                filter=(Q(registration__payment_completed=True) |
                        Q(registration__payment_deadline__gt=Now()))
            )
        )
        return queryset


class EventDetailView(generic.DetailView):
    model = Event
    context_object_name = "event"

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        queryset = Event.objects.filter(pk=pk).annotate(
            seats_taken=Count(
                "registration__event_id",
                filter=(Q(registration__payment_completed=True) |
                        Q(registration__payment_deadline__gt=Now()))
            )
        )
        return queryset


class EventSignUpConfirmationView(LoginRequiredMixin, generic.DetailView):
    model = Event
    context_object_name = "event"
    template_name = "event/event_confirmation.html"


class RegistrationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Registration
    fields = []

    def form_valid(self, form):
        event = Event.objects.filter(pk=self.kwargs["pk"]).annotate(
            seats_taken=Count(
                "registration__event_id",
                filter=(Q(registration__payment_completed=True) |
                        Q(registration__payment_deadline__gt=Now()))
            )
        ).first()
        if event.seats_taken >= event.max_occupancy:
            return redirect(reverse("admin:index"))  # TODO redirect to fail
        self.free_event = not bool(event.price)
        form.instance.event = event
        form.instance.user = self.request.user
        if not self.free_event:
            form.payment_completed = True
            form.payment_date = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        if self.free_event:
            return reverse("home:home")  # TODO redirect to completed
        return reverse("event:event_list")  # TODO redirect to payment page
