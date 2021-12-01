import pytest
from django.urls import reverse


class TestAnnouncementListView:

    @pytest.mark.parametrize("url", [
        "",
        reverse("home:home"),
    ])
    def test_response_code(self, client, url):
        response = client.get(url)

        assert response.status_code == 200
