from django.urls import path

from event import views


app_name = "event"
urlpatterns = [
    path("list", views.EventListView.as_view(), name="event_list"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event_details"),
]
