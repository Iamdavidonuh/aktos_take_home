"""
ASGI config for aktos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

settings_path = os.environ.get(
    "DJANGO_SETTINGS_MODULE", "aktos.settings.local_settings"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_path)

application = get_asgi_application()
