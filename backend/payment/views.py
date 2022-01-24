import json
from decimal import Decimal

from django.contrib.auth import mixins
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from payments import get_payment_model, RedirectNeeded
from payments.models import PaymentStatus

from config import settings
from payment.models import Payment
from event.models import Registration


class PaymentDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = get_payment_model()

    # TODO: check permissions, only registration owner can see payment content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PaymentStatus'] = PaymentStatus
        context['redirect_url'] = json.loads(
            self.object.extra_data)['card_response']['redirectUri']
        return context


class PaymentCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = get_payment_model()
    registration = None
    fields = ['billing_first_name', 'billing_last_name']

    def get(self, *args, **kwargs):
        registration = get_object_or_404(Registration, pk=self.kwargs["pk"])
        try:
            existing_payment = Payment.objects.get(registration_id=registration.id)
            return redirect(reverse('payment:details', kwargs={'pk': existing_payment.id}))
        except ObjectDoesNotExist:
            pass
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registration = get_object_or_404(Registration, pk=self.kwargs["pk"])
        context["registration"] = registration
        return context

    def form_valid(self, form):
        registration = get_object_or_404(Registration, pk=self.kwargs["pk"])
        try:
            existing_payment = Payment.objects.get(registration_id=registration.id)
            return redirect(reverse('payment:details', kwargs={'pk': existing_payment.id}))
        except ObjectDoesNotExist:
            pass

        if registration.user.id != self.request.user.id:
            return redirect(reverse("payment:wrong_user"))
        form.instance.variant = "default"
        form.instance.description = f"Ticket for {registration.event.title}"
        form.instance.total = Decimal(registration.event.price)
        form.instance.tax = Decimal(
            registration.event.price * Decimal(settings.PAYMENT_TICKET_TAX))
        form.instance.currency = 'PLN'
        form.instance.delivery = Decimal(0)
        form.instance.billing_email = self.request.user.email
        form.instance.customer_ip_address = (self.request.META.get('HTTP_X_FORWARDED_FOR')
                                             or self.request.META.get('REMOTE_ADDR'))
        form.instance.registration = registration

        return super().form_valid(form)

    def get_success_url(self):
        self.object.save()
        try:
            self.object.get_form()
        except RedirectNeeded as redirect_to:
            return str(redirect_to)
        return reverse("payment:details", kwargs={"payment_id": self.object.pk})


class PaymentWrongUser(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = "payment/wrong_user.html"
    extra_context = {"message": "This registration is related to the other user.",
                     "title": "Payment Failed"}


class PaymentSuccess(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = "payment/payment_success.html"
    model = get_payment_model()


class PaymentFailed(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = "payment/payment_failed.html"
    model = get_payment_model()
