from .models import Order, OrderItem
from books.models import Book

def create_order_from_cart(cart, user):
    """
    Given a cart dict and a user, create an Order and corresponding OrderItems.
    Returns the created Order instance.
    """
    # Calculate total amount
    total = 0
    for key, entry in cart.items():
        try:
            book = Book.objects.get(pk=int(key))
        except Book.DoesNotExist:
            continue
        qty = int(entry.get('qty', 0))
        price = getattr(book, 'price', 0) or 0
        total += qty * float(price)
    # Create order record
    order = Order.objects.create(user=user, total_amount=total)
    # Create OrderItems
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
    return order
