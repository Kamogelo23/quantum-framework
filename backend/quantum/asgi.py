"""
ASGI config for Quantum project.
Enables Django Channels for WebSocket support.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantum.settings')

django_asgi_app = get_asgi_application()

import apps.realtime.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                apps.realtime.routing.websocket_urlpatterns
            )
        )
    ),
})
