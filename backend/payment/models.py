from django.db import models

# Create your models here.
from decimal import Decimal

from django.urls import reverse
from payments import PurchasedItem
from payments.models import BasePayment

from config import settings


class Payment(BasePayment):

    def get_failure_url(self):
        return reverse("payment:failed", kwargs={'pk': self.pk})

    def get_success_url(self):
        return reverse("payment:success", kwargs={'pk': self.pk})

    registration = models.OneToOneField("event.Registration", on_delete=models.DO_NOTHING, null=True, blank=True)

    def get_purchased_items(self):
        return [PurchasedItem(name="Ticket",
                            quantity=1,
                            price=self.registration.event.price,
                            currency=self.currency,
                            sku='default',
                            tax_rate=Decimal(settings.PAYMENT_TICKET_TAX))]
