from django.urls import path
from argusflix_manager.consumers import MyWebSocketConsumer
from apps.devices.consumers import DeviceWebSocketConsumer

websocket_urlpatterns = [
    path("ws/", MyWebSocketConsumer.as_asgi()),
    path("ws/device/<str:device_id>/", DeviceWebSocketConsumer.as_asgi()),
]
