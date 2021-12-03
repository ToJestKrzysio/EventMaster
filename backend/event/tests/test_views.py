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
        templates = {temp.name for temp
                     in event_detail_view_response.templates}

        assert "base.html" in templates
        assert "event/event_detail.html" in templates

    def test_response_context(self, event_detail_view_response):
        event = event_detail_view_response.context["event"]

        assert event.seats_taken == 1
