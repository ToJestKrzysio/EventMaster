from django.db.models.functions import Now
from django.views import generic

from home import models


class AnnouncementListView(generic.ListView):
    # model = models.Announcement
    context_object_name = "announcements"
    queryset = models.Announcement.objects.filter(
        publish_date__lte=Now(),
        hide_date__gte=Now(),
    ).order_by("-pinned", "publish_date")
