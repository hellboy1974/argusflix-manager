import django
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import argusflix_manager.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "argusflix_manager.settings")
django.setup()

from .jwt_ws_auth import JWTAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(argusflix_manager.routing.websocket_urlpatterns)
    ),
})
