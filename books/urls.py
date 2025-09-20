from django.urls import path
from .views import book_detail, book_list

app_name = "books"

urlpatterns = [
    path("", book_list, name="book_list"),
    path("<slug:slug>/", book_detail, name="book_detail"),
]