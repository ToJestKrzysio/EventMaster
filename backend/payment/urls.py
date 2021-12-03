from django.urls import path

from payment import views


app_name = "payment"
urlpatterns = [
    path("pay", views.pay, name="pay"),
    path("create_payment", views.create_payment, name="create_payment"),
    path("success", views.success, name="success"),
    path("failure", views.failure, name="failure")
]
