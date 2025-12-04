from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from .models import Book
from django.core.paginator import Paginator


def home(request):
    return render(request, "home.html")

# Create your views here.
def book_detail(request,slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "books/book_detail.html", {"book": book})

def book_list(request):
    # Search filter
    q = request.GET.get('q', '').strip()
    qs = Book.objects.all()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(isbn__icontains=q) |
            Q(description__icontains=q)
        )

    # Server-side pagination used for infinite scroll batches
    paginator = Paginator(qs.order_by('id'), 12)  # 12 per batch
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    # If this is an infinite-scroll request, return only the cards HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('load') == '1':
        html = render_to_string(
            'books/partials/_book_cards.html',
            { 'page_obj': page_obj },
            request=request
        )
        return HttpResponse(html)

    # Initial page render
    context = {
        'page_obj': page_obj,
        'q': q,
        'has_next': page_obj.has_next(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    }
    return render(request, "books/book_list.html", context)