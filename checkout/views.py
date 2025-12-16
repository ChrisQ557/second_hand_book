from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
import stripe
from cart.services import _get_cart, total_qty
from books.models import Book

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


def checkout_success(request):
    return render(request, 'checkout/success.html')


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
