from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from event.models import Event, Registration


@pytest.fixture
def event_db(db):
    user = get_user_model().create(
        username="testuser",
        password="NotVeryStrongPassword",
        email="testmail@testmail.com"
    )
    event = Event.objects.create(
        title="Test Event",
        description="This is test Event",
        start_time=timezone.now(),
        end_time=timezone.now(),
        registration_deadline=timezone.now(),
        price=666,
        max_occupancy=13,
        location="D2 404",
    )
    Registration.objects.create(
        event=event, user=user,
        payment_completed=False,
        payment_deadline=timezone.now() + timedelta(days=2),
    )


@pytest.fixture
def event_list_view_response(client, db):
    return client.get(reverse("event:event_list"))
