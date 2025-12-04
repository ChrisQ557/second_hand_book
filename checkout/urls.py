from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("", views.checkout_view, name="view"),
    path("create-session/", views.checkout_create_session, name="create_session"),
]
