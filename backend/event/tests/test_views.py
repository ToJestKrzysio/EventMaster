import pytest
from django.urls import reverse


class TestEventListView:

    @pytest.mark.parametrize("url", [
        "/event/list",
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
        print(event_list_view_response.context["events"])
        assert False
        # event_list =
        #
        # for event in event_list:
        #     assert event.seats_taken == 1
