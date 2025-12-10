from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
from django.db import models


class Book(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("es", "Spanish"),
        ("de", "German"),
        ("it", "Italian"),
        ("sv", "Swedish"),
    ]

    GENRE_CHOICES = [
        ("fiction", "Fiction"),
        ("non_fiction", "Non-Fiction"),
        ("fantasy", "Fantasy"),
        ("sci_fi", "Sci-Fi"),
        ("mystery", "Mystery"),
        ("biography", "Biography"),
        ("history", "History"),
        ("children", "Children"),
        ("romance", "Romance"),
        ("classics", "Classics"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    cover = models.ImageField(upload_to="book_covers/", null=True, blank=True)
    # New static-based cover path used by WhiteNoise
    cover_path = models.CharField(max_length=255, blank=True, null=True, help_text="Static path like 'images/covers/es/my-book.jpg'")

    slug = models.SlugField(max_length=200, unique=True)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    description = models.TextField(blank=True)

    # New metadata fields
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default="other")
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default="en")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not already set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
