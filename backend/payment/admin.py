from django.contrib import admin

# Register your models here.
from payment import models


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id", "billing_first_name", "billing_last_name", "total", "billing_email",
    )

    # form = EventForm


admin.site.register(models.Payment, PaymentAdmin)
