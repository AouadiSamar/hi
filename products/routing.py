# product/routing.py
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import ProductNotificationConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"ws/notifications/$", ProductNotificationConsumer.as_asgi()),
        ])
    ),
})
