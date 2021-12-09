import pytest
from django.urls import reverse


class TestEventListView:

    @pytest.mark.parametrize("url", [
        "/event/",
        reverse("event:event_list")
    ])
    def test_status_code(self, client, db, url):
        response = client.get(url)

        assert response.status_code == 200

    def test_response_template(self, event_list_view_response):
        templates = {temp.name for temp in event_list_view_response.templates}

        assert "base.html" in templates
        assert "event/event_list.html" in templates

    def test_response_context(self, event_list_view_response):
        context = event_list_view_response.context["events"]
        for event in context:
            assert event.seats_taken == 1


class TestEventDetailView:

    @pytest.mark.parametrize("url", [
        "/event/1",
        reverse("event:event_detail", kwargs={"pk": 1}),
    ])
    def test_status_code(self, url, client, event_db):
        response = client.get(url)

        assert response.status_code == 200

    def test_response_template(self, event_detail_view_response):
        templates = {temp.name for temp in
                     event_detail_view_response.templates}

        assert "base.html" in templates
        assert "event/event_detail.html" in templates

    def test_response_context(self, event_detail_view_response):
        event = event_detail_view_response.context["event"]

        assert event.title == "Test Event"
        assert event.description == "This is test Event"
        assert event.price == 666
        assert event.max_occupancy == 13
        assert event.location == "D2 404"
        assert event.seats_taken == 1


class TestEventConfirmationView:

    @pytest.mark.parametrize("url", [
        "/event/sign_up/1",
        reverse("event:event_sign_up", kwargs={"pk": 1})
    ])
    def test_response_code_unauthenticated(self, client, event_db, url):
        response = client.get(url)

        assert response.status_code == 302

    @pytest.mark.parametrize("url", [
        "/event/sign_up/1",
        reverse("event:event_sign_up", kwargs={"pk": 1})
    ])
    def test_response_code_authenticated(self, client, event_db, db_user, url):
        client.force_login(db_user)
        response = client.get(url)

        assert response.status_code == 200

    def test_response_template(self, event_confirmation_view_response):
        templates = {temp.name for temp in
                     event_confirmation_view_response.templates}

        assert "base.html" in templates
        assert "event/event_confirmation.html" in templates

    def test_response_context(self, event_confirmation_view_response):
        event = event_confirmation_view_response.context["event"]

        assert event.title == "Test Event"
        assert event.description == "This is test Event"
        assert event.price == 666
        assert event.max_occupancy == 13
        assert event.location == "D2 404"


class TestRegistrationCreateView:

    @pytest.mark.parametrize("url", [
        "/event/register/1",
        reverse("event:register", kwargs={"pk": 1}),
    ])
    def test_response_code_unauthorized(self, client, event_db, url):
        response = client.post(url)

        assert response.status_code == 302
        assert reverse("account_login") in response.url

    @pytest.mark.parametrize("url", [
        "/event/register/1",
        reverse("event:register", kwargs={"pk": 1}),
    ])
    def test_response_code_authorized(self, client, event_db, db_user, url):
        client.force_login(db_user)
        response = client.post(url)

        assert response.status_code == 302
        assert reverse("account_login") not in response.url


class TestRegistrationSuccessfulView:

    @pytest.mark.parametrize("url", [
        "/event/register_success/1",
        reverse("event:register_success", kwargs={"pk": 1}),
    ])
    def test_response_code_unauthorized(self, client, event_db, url):
        response = client.get(url)

        assert response.status_code == 302

    @pytest.mark.parametrize("url", [
        "/event/register_success/1",
        reverse("event:register_success", kwargs={"pk": 1}),
    ])
    def test_response_code_authenticated(self, client, event_db, db_user, url):
        client.force_login(db_user)
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.parametrize("url", [
        "/event/register_success/1",
        reverse("event:register_success", kwargs={"pk": 1}),
    ])
    def test_response_payment_incomplete(self, client, event_db, url):
        user, _, _, registration = event_db
        registration.payment_completed = False
        registration.save()
        client.force_login(user)
        response = client.get(url)

        assert response.status_code == 302
        assert response.url == reverse(
            "home:home")  # TODO failed reservation redirect

    def test_response_template(self, event_registration_successful_response):
        templates = {temp.name for temp in
                     event_registration_successful_response.templates}

        assert "base.html" in templates
        assert "event/registration_successful.html" in templates


class TestRegistrationIncompleteView:

    @pytest.mark.parametrize("url", [
        "/event/register_failed",
        reverse("event:register_failed"),
    ])
    def test_response_code_unauthorized(self, client, event_db, url):
        response = client.get(url)

        assert response.status_code == 302
        assert reverse("account_login") in response.url

    @pytest.mark.parametrize("url", [
        "/event/register_failed",
        reverse("event:register_failed"),
    ])
    def test_response_code_authenticated(self, client, event_db, db_user, url):
        client.force_login(db_user)
        response = client.get(url)

        assert response.status_code == 200

    def test_response_template(self, event_registration_failed_response):
        templates = {temp.name for temp in
                     event_registration_failed_response.templates}

        assert "base.html" in templates
        assert "event/registration_failed.html" in templates
