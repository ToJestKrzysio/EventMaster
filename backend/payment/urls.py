from django.urls import path

from payment import views

app_name = "payment"
urlpatterns = [
    # path("<int:pk>", views.EventDetailView.as_view(), name="event_detail"),
    path("create/<int:pk>", views.PaymentCreateView.as_view(),
         name="create"),
    path("<int:pk>", views.PaymentDetailView.as_view(),
         name="details"),
    path("wrong_user", views.PaymentWrongUser.as_view(),
         name="wrong_user"),
    path("success/<int:pk>", views.PaymentSuccess.as_view(), name="success"),
    path("failed/<int:pk>", views.PaymentFailed.as_view(), name="failed"),

]
