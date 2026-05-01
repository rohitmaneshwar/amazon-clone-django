"""
WSGI config for amazon_clone project.
"""

import os

from django.core.wsgi import get_wsgi_application

# Yahan 'amazon_clone' tumhare project ka naam hai
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazon_clone.settings')

application = get_wsgi_application()