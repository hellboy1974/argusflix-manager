from django.urls import path
from argusflix_manager.consumers import MyWebSocketConsumer

websocket_urlpatterns = [
    path("ws/", MyWebSocketConsumer.as_asgi()),
]
