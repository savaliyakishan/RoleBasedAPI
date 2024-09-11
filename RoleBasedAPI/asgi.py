"""
ASGI config for RoleBasedAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from entry_management.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RoleBasedAPI.settings')

import django
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':URLRouter(
        websocket_urlpatterns
    ),
})