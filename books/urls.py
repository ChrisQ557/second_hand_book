from django.urls import path
from .views import book_detail, book_list, add_to_bag

app_name = "books"

urlpatterns = [
    path("", book_list, name="book_list"),
    path("<slug:slug>/", book_detail, name="book_detail"),
    path("<slug:slug>/add-to-bag/", add_to_bag, name="add_to_bag"),
]