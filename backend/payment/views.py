import json
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import generic
from payments import get_payment_model, RedirectNeeded

from payment.models import Payment

# def payment_details(request, payment_id):
#     payment = get_object_or_404(get_payment_model(), id=payment_id)
#     try:
#         form = payment.get_form(data=request.POST or None)
#     except RedirectNeeded as redirect_to:
#         return redirect(str(redirect_to))
#     return TemplateResponse(request, 'payment.html',
#                             {'form': form, 'payment': payment})
from config import settings

from event.models import Registration
from payments.models import PaymentStatus


class PaymentDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_payment_model()

    # context_object_name = "event"
    # TODO: check permissions, only registration owner can see payment content

    def get_context_data(self, **kwargs):
        old = super().get_context_data(**kwargs)
        return {'PaymentStatus': PaymentStatus,
                'redirect_url': json.loads(self.object.extra_data)['card_response']['redirectUri'],
                **old}


class PaymentCreateView(LoginRequiredMixin, generic.CreateView):
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
        registration = get_object_or_404(Registration, pk=self.kwargs["pk"])

        return {
            'registration': registration,
        }

    def form_valid(self, form):
        registration = get_object_or_404(Registration, pk=self.kwargs["pk"])
        try:
            existing_payment = Payment.objects.get(registration_id=registration.id)
            return redirect(reverse('payment:details', kwargs={'pk': existing_payment.id}))
        except ObjectDoesNotExist:
            pass

        if registration.user.id != self.request.user.id:
            return redirect(reverse("payment:wrong_user"))
        # form.instance.variant = 'default'
        form.instance.variant = "default"
        form.instance.description = f"Ticket for {registration.event.title}"
        form.instance.total = Decimal(registration.event.price)
        form.instance.tax = Decimal(registration.event.price * Decimal(settings.PAYMENT_TICKET_TAX))
        form.instance.currency = 'PLN'
        form.instance.delivery = Decimal(0)
        form.instance.billing_email = self.request.user.email
        form.instance.customer_ip_address = self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get(
            'REMOTE_ADDR')
        form.instance.registration = registration

        return super().form_valid(form)

    def get_success_url(self):
        self.object.save()
        try:
            self.object.get_form()
        except RedirectNeeded as redirect_to:
            return str(redirect_to)
        return reverse("payment:details", kwargs={"payment_id": self.object.id})


class PaymentWrongUser(LoginRequiredMixin, generic.TemplateView):
    template_name = "payment/wrong_user.html"
    extra_context = {"message": "This registration is related with other user.",
                     "title": "Payment Failed"}


class PaymentSuccess(LoginRequiredMixin, generic.DetailView):
    template_name = "payment/payment_success.html"
    model = get_payment_model()


class PaymentFailed(LoginRequiredMixin, generic.DetailView):
    template_name = "payment/payment_failed.html"
    model = get_payment_model()
