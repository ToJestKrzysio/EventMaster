from django.contrib import admin

from event import models
from event.forms import EventForm
from event.models import Registration


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title", "location", "start_time", "end_time", "max_occupancy", "price",
    )
    form = EventForm

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "user", "event", "payment_completed"
    )
    model = Registration
    readonly_fields = (
        "modified_by",
    )

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Registration, RegistrationAdmin)
