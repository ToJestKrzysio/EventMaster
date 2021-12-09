from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from event.models import Event, Registration


@pytest.fixture
def db_user(db):
    return get_user_model().objects.create(
        username="testuser",
        password="NotVeryStrongPassword",
        email="testmail@testmail.com"
    )


@pytest.fixture
def db_user_2(db):
    return get_user_model().objects.create(
        username="testuser2",
        password="NotVeryStrongPassword",
        email="testmail@testmail2.com"
    )


@pytest.fixture
def db_admin(db):
    admin = get_user_model().objects.create(
        username="superuser",
        password="NotVeryStrongPassword",
        email="adminmail@testmail.com"
    )
    admin.superuser = True
    admin.save()
    return admin


@pytest.fixture
def db_event(db_admin):
    return Event.objects.create(
        title="Test Event",
        description="This is test Event",
        start_time=timezone.now(),
        end_time=timezone.now(),
        registration_deadline=timezone.now(),
        price=666,
        max_occupancy=13,
        location="D2 404",
        creator=db_admin,
        pk=1,
    )


@pytest.fixture
def db_free_event(db_admin):
    return Event.objects.create(
        title="Test Free Event",
        description="This is test Event",
        start_time=timezone.now(),
        end_time=timezone.now(),
        registration_deadline=timezone.now(),
        price=0,
        max_occupancy=13,
        location="D2 404",
        creator=db_admin,
        pk=2,
    )


@pytest.fixture
def db_registration(db_user, db_event):
    return Registration.objects.create(
        event=db_event, user=db_user,
        payment_completed=True,
        payment_deadline=timezone.now() + timedelta(days=2),
       )


@pytest.fixture
def event_db(db_user, db_admin, db_event, db_registration):
    return db_user, db_admin, db_event, db_registration


@pytest.fixture
def event_list_view_response(client, event_db):
    return client.get(reverse("event:event_list"))


@pytest.fixture
def event_detail_view_response(client, event_db):
    return client.get(reverse("event:event_detail", kwargs={"pk": 1}))


@pytest.fixture
def event_confirmation_view_response(client, event_db, db_user):
    client.force_login(db_user)
    return client.get(reverse("event:event_sign_up", kwargs={"pk": 1}))


@pytest.fixture
def event_registration_successful_response(client, event_db, db_user):
    client.force_login(db_user)
    return client.get(reverse("event:register_success", kwargs={"pk": 1}))


@pytest.fixture
def event_registration_failed_response(client, event_db, db_user):
    client.force_login(db_user)
    return client.get(reverse("event:register_failed"))


@pytest.fixture
def event_registration_payment_incomplete_response(client, event_db, db_user):
    client.force_login(db_user)
    return client.get(reverse("event:register_payment_incomplete"))


@pytest.fixture
def event_registration_max_occupancy_response(client, event_db, db_user):
    client.force_login(db_user)
    return client.get(reverse("event:register_max_occupancy"))


@pytest.fixture
def user_events_list_response(client, event_db, db_user):
    client.force_login(db_user)
    return client.get(reverse("event:user_events_list"))
