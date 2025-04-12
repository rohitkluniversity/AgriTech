"""
WSGI config for agritech project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agritech.settings')

application = get_wsgi_application()
