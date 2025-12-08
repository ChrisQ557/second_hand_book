"""
WSGI config for second_hand_book project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_hand_book.settings')

# Diagnostic: print which settings module is used at runtime (appears in Heroku logs)
try:
    import sys
    print("DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"), file=sys.stderr)
except Exception:
    pass

application = get_wsgi_application()
