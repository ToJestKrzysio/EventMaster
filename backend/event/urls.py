from django.urls import path

from event import views

app_name = "event"
urlpatterns = [
    path("", views.EventListView.as_view(), name="event_list"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event_detail"),
    path("sign_up/<int:pk>", views.EventSignUpConfirmationView.as_view(),
         name="event_sign_up"),
    path("register/<int:pk>", views.RegistrationCreateView.as_view(),
         name="register")
]
