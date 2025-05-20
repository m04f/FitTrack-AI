from channels.routing import URLRouter
from django.urls import re_path, path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path(r"ws/chat/<uuid:session>/", ChatConsumer.as_asgi())
]
