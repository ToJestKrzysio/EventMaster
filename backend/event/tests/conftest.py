import pytest
from django.urls import reverse
from django.utils import timezone

from event.models import Event


@pytest.fixture
def event_db(db):
    Event.objects.create(
        title="Test Event",
        description="This is test Event",
        start_time=timezone.now(),
        duration=30,
        price=666,
        max_occupancy=13,
        location="D2 404",
    )


@pytest.fixture
def event_list_view_response(client, db):
    return client.get(reverse("event:event_list"))
