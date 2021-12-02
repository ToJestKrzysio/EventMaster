import pytest
from django.urls import reverse


class TestAnnouncementListView:

    @pytest.mark.parametrize("url", [
        "",
        reverse("home:home"),
    ])
    def test_response_code(self, client, db, url):
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.parametrize("url", [
        "",
        reverse("home:home"),
    ])
    def test_response_template(self, client, db, url):
        response = client.get(url)
        templates = {template.name for template in response.templates}

        assert "base.html" in templates
        assert "home/announcement_list.html" in templates
