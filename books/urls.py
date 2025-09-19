from django.urls import path
from .views import book_detail

app_name = "books"

urlpatterns = [
    path("<slug:slug>/", book_detail, name="book_detail"),
]