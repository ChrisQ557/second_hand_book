from django.conf import settings
from django.db import models
from books.models import Book


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Processing")
    # whether the user has marked the order as received
    received = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.email} – {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}×{self.book.title} (Order {self.order_id})"
