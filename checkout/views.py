from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from cart.services import _get_cart, total_qty
from books.models import Book


def checkout_view(request):
    cart = _get_cart(request.session)
    if not cart:
        return redirect('cart:view')
    items = []
    subtotal = 0
    for key, entry in cart.items():
        try:
            book = Book.objects.get(pk=int(key))
        except Book.DoesNotExist:
            # Skip missing items
            continue
        qty = int(entry.get('qty', 0))
        price = getattr(book, 'price', 0) or 0
        line_total = qty * float(price)
        subtotal += line_total
        items.append({
            'book': book,
            'qty': qty,
            'price': price,
            'line_total': line_total,
        })
    context = {
        'items': items,
        'subtotal': subtotal,
        'count': total_qty(request.session),
    }
    return render(request, 'checkout/checkout.html', context)


@require_POST
def checkout_create_session(request):
    # Placeholder: later create Stripe Checkout Session here
    # For now, redirect back to checkout page to show it's wired
    return redirect('checkout:view')
