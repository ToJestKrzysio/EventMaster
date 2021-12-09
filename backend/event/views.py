from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from event.exceptions import PaymentIncompleteException
from event.models import Event, Registration


class EventListView(generic.ListView):
    model = Event
    context_object_name = "events"
    template_name = "event/event_list.html"
    queryset = Event.objects_with_registrations.all()


class EventDetailView(generic.DetailView):
    model = Event
    context_object_name = "event"

    def get_queryset(self, *args, **kwargs):
        return Event.objects_with_registrations.filter(pk=self.kwargs["pk"])


class EventSignUpConfirmationView(LoginRequiredMixin, generic.DetailView):
    model = Event
    context_object_name = "event"
    template_name = "event/event_confirmation.html"


class RegistrationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Registration
    fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.free_event = False

    def form_valid(self, form):
        event = Event.objects_with_registrations.get(pk=self.kwargs["pk"])
        self.free_event = not bool(event.price)
        already_registered = Registration.objects.filter(
            event_id=self.kwargs["pk"], user_id=self.request.user.id)
        if already_registered:
            return redirect(reverse(
                "event:register_success", kwargs={"pk": self.kwargs["pk"]}))
        if event.seats_taken >= event.max_occupancy:
            return redirect(reverse("event:register_max_occupancy"))
        form.instance.event = event
        form.instance.user = self.request.user
        if self.free_event:
            form.instance.payment_completed = True
            form.instance.payment_date = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        if self.free_event:
            return reverse("event:register_success",
                           kwargs={"pk": self.kwargs["pk"]})
        return reverse(
            "event:register_failed")  # TODO redirect to payment page


class RegistrationSuccessfulView(LoginRequiredMixin, generic.DetailView):
    context_object_name = "registration"
    template_name = "event/registration_successful.html"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except PaymentIncompleteException:
            return redirect(reverse("event:register_payment_incomplete"))
        except Http404:
            return redirect(reverse("event:register_failed"))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        event_pk = self.kwargs["pk"]
        user = self.request.user
        registrations = Registration.objects.select_related("event").filter(
            user_id=user.id, event_id=event_pk)
        if not registrations:
            raise Http404("No registration found!")
        try:
            registration = registrations.get(payment_completed=True)
        except Registration.DoesNotExist:
            raise PaymentIncompleteException("payment incomplete.")
        return registration


class RegistrationFailedView(LoginRequiredMixin, generic.TemplateView):
    template_name = "event/registration_incomplete.html"
    extra_context = {"message": "Looks like something went wrong during "
                                "your registration attempt.",
                     "title": "Registration Failed"}


class RegistrationPaymentIncompleteView(LoginRequiredMixin,
                                        generic.TemplateView):
    template_name = "event/registration_incomplete.html"
    extra_context = {"message": "The payment have not been completed or is "
                                "still being processed.",
                     "title": "Payment Incomplete"}


class RegistrationMaxOccupancyView(LoginRequiredMixin, generic.TemplateView):
    template_name = "event/registration_incomplete.html"
    extra_context = {"message": "This event has already maximum occupancy.",
                     "title": "Registration Failed"}
