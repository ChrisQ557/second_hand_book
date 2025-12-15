from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.shortcuts import redirect
from .models import Book
from django.core.paginator import Paginator


def home(request):
    return render(request, "home.html")


def add_to_bag(request, slug):
    if request.method != 'POST':
        return redirect('books:book_detail', slug=slug)
    # Initialize and increment session cart_count
    count = request.session.get('cart_count', 0)
    request.session['cart_count'] = count + 1
    request.session.modified = True
    return redirect('books:book_detail', slug=slug)

# Create your views here.
def book_detail(request,slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "books/book_detail.html", {"book": book})

def book_list(request):
    # Search & filters
    q = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()
    author = request.GET.get('author', '').strip()
    language = request.GET.get('language', '').strip()

    qs = Book.objects.all()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(isbn__icontains=q) |
            Q(description__icontains=q)
        )
    if genre:
        qs = qs.filter(genre=genre)
    if author:
        qs = qs.filter(author__icontains=author)
    if language:
        qs = qs.filter(language=language)

    # Render ALL books (no pagination)
    page_obj = qs.order_by('id')

    # Initial page render with full list
    context = {
        'page_obj': page_obj,
        'q': q,
        'genre': genre,
        'author': author,
        'language': language,
        'genre_choices': Book.GENRE_CHOICES,
        'language_choices': Book.LANGUAGE_CHOICES,
    }
    return render(request, "books/book_list.html", context)