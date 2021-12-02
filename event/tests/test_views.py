import pytest
from django.urls import reverse


class TestEventListView:

    @pytest.mark.parametrize("url", [
        "/event_list/",
        reverse("event:event_list")
    ])
    def test_status_code(self, client, url):
        response = client.get(url)

        assert response.status_code == 200

    def test_response_template(self, event_list_view_response):
        templates = {temp.name for temp in event_list_view_response.templates}

        assert "base.html" in templates
        assert "event/event_list.html" in templates

    def test_response_context(self, event_list_view_response):
        event_list = event_list_view_response.context['event_list']

        for event in event_list:
            assert event.details is not None
