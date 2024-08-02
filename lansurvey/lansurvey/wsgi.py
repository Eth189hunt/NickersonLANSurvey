"""
WSGI config for lansurvey project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

import dotenv
from django.core.wsgi import get_wsgi_application

base = Path(__file__).resolve().parent.parent
dotenv.read_dotenv(base)
print(os.environ.get("SECRET_KEY"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lansurvey.settings")

application = get_wsgi_application()
