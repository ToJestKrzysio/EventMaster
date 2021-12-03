from django.db import models
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from event.models import Registration
from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment


class Payment(BasePayment):
    registration = models.ForeignKey(Registration, on_delete=models.DO_NOTHING, editable=False)

    get_failure_url = reverse_lazy('payment:success')

    success_url = reverse_lazy('payment:failure')

    def get_purchased_items(self):
        # you'll probably want to retrieve these from an associated order
        yield []
