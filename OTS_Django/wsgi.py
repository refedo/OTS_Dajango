"""
WSGI config for OTS_Django project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OTS_Django.settings')

application = get_wsgi_application()
