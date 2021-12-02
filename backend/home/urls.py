from django.urls import path

from home import views


app_name = "home"
urlpatterns = [
    path("", views.AnnouncementListView.as_view(), name="home"),
]
