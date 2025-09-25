from django.db import models
from django.utils.text import slugify

# Create your models here.
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not already set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
