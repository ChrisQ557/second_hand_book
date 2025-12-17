from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("", views.checkout_view, name="view"),
    path("create-payment-intent/", views.create_payment_intent, name="create_payment_intent"),
    path("success/", views.checkout_success, name="success"),
    path("history/", views.order_history, name="history"),
    path("<int:order_id>/delete/", views.delete_order, name="delete"),
    path("<int:order_id>/received/", views.mark_received, name="received"),
]
