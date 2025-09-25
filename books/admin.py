from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Book

@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    list_display       = ('title', 'author', 'published_date', 'isbn', 'slug')
    prepopulated_fields= {'slug': ('title',)}
    summernote_fields  = ('description',) 

