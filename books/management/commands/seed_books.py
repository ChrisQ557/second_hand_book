import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from books.models import Book
from faker import Faker
import urllib.request

class Command(BaseCommand):
    help = "Seed the database with fake second-hand books."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help='Number of books to seed')

    def handle(self, *args, **options):
        fake = Faker()

        for i in range(options['count']):
            title = fake.sentence(nb_words=5).rstrip('.')
            author = fake.name()
            isbn = fake.isbn13(separator="")
            published_date = fake.date_between(start_date='-50y', end_date='today')
            description = fake.paragraph(nb_sentences=5)

            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                published_date=published_date,
                description=description,
            )
            book.save()  # slug auto-generated

            # Download a random cover and attach
            img_url = f"https://picsum.photos/200/300?random={i}"
            temp_path, _ = urllib.request.urlretrieve(img_url)
            with open(temp_path, 'rb') as img_file:
                book.cover.save(f"cover_{i}.jpg", File(img_file), save=True)

        self.stdout.write(self.style.SUCCESS(f"Seeded {options['count']} books successfully."))
