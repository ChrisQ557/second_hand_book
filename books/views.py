from django.shortcuts import render, get_object_or_404
from .models import Book
from django.core.paginator import Paginator

# Create your views here.
def book_detail(request,slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "books/book_detail.html", {"book": book})

def book_list(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 6)  # 6 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "books/book_list.html", {"page_obj": page_obj})