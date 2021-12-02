from django.contrib import admin

from event import models


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title", "location", "start_time", "duration", "max_occupancy",
        "current_occupancy"
    )
    fields = [
        "title", "description", "start_time", "duration", "price",
        "max_occupancy", "location"
    ]

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class RegistrationAdmin(admin.ModelAdmin):
    fields = ["Event", "User", "payment_completed", "payment_date",
              "payment_deadline"]


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Registration, RegistrationAdmin)
