from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from books.models import Book
from .services import add_item, update_item, remove_item, _get_cart, total_qty


def cart_view(request):
    cart = _get_cart(request.session)
    items = []
    subtotal = 0
    # Minimal subtotal: if Book lacks price, treat as 0
    for key, entry in cart.items():
        book = get_object_or_404(Book, pk=int(key))
        qty = int(entry.get("qty", 0))
        price = getattr(book, "price", 0) or 0
        line_total = qty * float(price)
        subtotal += line_total
        items.append({
            "book": book,
            "qty": qty,
            "price": price,
            "line_total": line_total,
        })
    context = {
        "items": items,
        "subtotal": subtotal,
        "count": total_qty(request.session),
    }
    return render(request, "cart/cart.html", context)


@require_POST
def cart_add(request, slug):
    book = get_object_or_404(Book, slug=slug)
    add_item(request.session, book.id, 1)
    messages.success(request, f'Added “{book.title}” to your bag.')
    return redirect("books:book_detail", slug=slug)


@require_POST
def cart_update(request, slug):
    book = get_object_or_404(Book, slug=slug)
    try:
        qty = int(request.POST.get("qty", 1))
    except ValueError:
        qty = 1
    update_item(request.session, book.id, qty)
    messages.success(request, f'Updated “{book.title}” quantity to {qty}.')
    return redirect("cart:view")


@require_POST
def cart_remove(request, slug):
    book = get_object_or_404(Book, slug=slug)
    remove_item(request.session, book.id)
    messages.info(request, f'Removed “{book.title}” from your bag.')
    return redirect("cart:view")
