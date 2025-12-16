from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("", views.checkout_view, name="view"),
    path("create-payment-intent/", views.create_payment_intent, name="create_payment_intent"),
    path("success/", views.checkout_success, name="success"),
]
