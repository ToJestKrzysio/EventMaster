from django.core.exceptions import ValidationError
from django.forms import ModelForm

from event.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time",
                  "registration_deadline", "price", "max_occupancy",
                  "location"]

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError("Price cannot be negative.")
        return price

    def clean_max_occupancy(self):
        max_occupancy = self.cleaned_data["max_occupancy"]
        if max_occupancy < 0:
            raise ValidationError("Maximum occupancy cannot be negative.")
        if not isinstance(max_occupancy, int):
            raise ValidationError(
                "Maximum occupancy has to be an integer value.")
        return max_occupancy

    def clean_end_time(self):
        start_time = self.cleaned_data["start_time"]
        end_time = self.cleaned_data["end_time"]
        if start_time >= end_time:
            raise ValidationError("End time can't be lower than start time.")
        return end_time

    def clean_registration_deadline(self):
        start_time = self.cleaned_data["start_time"]
        registration_deadline = self.cleaned_data["registration_deadline"]
        if registration_deadline >= start_time:
            raise ValidationError(
                "Registration deadline can't be greater than start time.")
        return registration_deadline
