from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from payments import get_payment_model, RedirectNeeded
from django.http import HttpResponseRedirect

from config import settings

from event.models import Registration


# TODO: copied piece of code, don't know how it works
def pay(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'payment.html',
                            {'form': form, 'payment': payment})


# TODO: notification when registration is for free
def create_payment(request): #
    # payment = get_object_or_404(Registration, id=registration_id)
    # if payment.price == 0:
    #     return redirect(request.META.get('HTTP_REFERER'))

    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant=settings.PAYMENT_VARIANTS['payu'][0],
        description='Book purchase',
        total=Decimal(20), #payment.event.price
        tax=Decimal(5), #payment.event.price * settings.TICKET_TAX_RATE
        currency='PLN',
        delivery=Decimal(0)
    )

    return redirect(reverse('payment:make_payment'))

def success(request):
    return render(request,'payment/success.html')

def failure(request):
    return render(request,'payment/failure.html')

