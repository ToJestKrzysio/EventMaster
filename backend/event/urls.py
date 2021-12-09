from django.urls import path

from event import views

app_name = "event"
urlpatterns = [
    path("", views.EventListView.as_view(), name="event_list"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event_detail"),
    path("sign_up/<int:pk>", views.EventSignUpConfirmationView.as_view(),
         name="event_sign_up"),
    path("register/<int:pk>", views.RegistrationCreateView.as_view(),
         name="register"),
    path("register_success/<int:pk>",
         views.RegistrationSuccessfulView.as_view(), name="register_success"),
    path("register_failed", views.RegistrationFailedView.as_view(),
         name="register_failed"),
    path("register_payment_incomplete",
         views.RegistrationPaymentIncompleteView.as_view(),
         name="register_payment_incomplete"),
    path("register_max_occupancy",
         views.RegistrationMaxOccupancyView.as_view(),
         name="register_max_occupancy"),
]
