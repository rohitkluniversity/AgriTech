"""
ASGI config for agritech project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agritech.settings')

application = get_asgi_application()
