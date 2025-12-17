from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
import stripe
from cart.services import _get_cart, total_qty
from books.models import Book
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


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
    context.update({
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'STRIPE_CURRENCY': settings.STRIPE_CURRENCY,
    })
    return render(request, 'checkout/checkout.html', context)


@login_required
def checkout_success(request):
    cart = _get_cart(request.session)
    order = None
    if cart:
        total = sum(
            int(entry.get('qty', 0)) * (getattr(Book.objects.get(pk=int(key)), 'price') or 0)
            for key, entry in cart.items()
        )
        order = Order.objects.create(user=request.user, total_amount=total)
        for key, entry in cart.items():
            try:
                book = Book.objects.get(pk=int(key))
            except Book.DoesNotExist:
                continue
            qty = int(entry.get('qty', 0))
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=qty,
                price_at_purchase=book.price or 0,
            )
    # Clear the cart from session
    if 'cart' in request.session:
        try:
            del request.session['cart']
        except Exception:
            request.session['cart'] = {}
        request.session.modified = True
    return render(request, 'checkout/success.html', {'order': order})


@csrf_exempt
@require_POST
def create_payment_intent(request):
    cart = _get_cart(request.session)
    if not cart:
        return HttpResponseBadRequest('Cart is empty')

    subtotal = Decimal('0')
    for key, entry in cart.items():
        try:
            book = Book.objects.get(pk=int(key))
        except Book.DoesNotExist:
            continue
        qty = int(entry.get('qty', 0))
        price = Decimal(str(getattr(book, 'price', 0) or 0))
        subtotal += (price * qty)

    if subtotal <= 0:
        return HttpResponseBadRequest('Invalid total')

    currency = (settings.STRIPE_CURRENCY or 'USD').lower()
    amount = int((subtotal * 100).to_integral_value(rounding=ROUND_HALF_UP))

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )
        return JsonResponse({
            'clientSecret': intent['client_secret'],
            'publishableKey': settings.STRIPE_PUBLIC_KEY,
            'amount': amount,
            'currency': currency,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def order_history(request):
    orders = request.user.orders.prefetch_related("items__book").order_by("-order_date")
    return render(request, "account/order_history.html", {"orders": orders})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order.delete()
    return redirect('checkout:history')

@login_required
def mark_received(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order.received = True
    order.save()
    return redirect('checkout:history')
