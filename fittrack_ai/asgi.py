"""
ASGI config for fittrack_ai project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_ai.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     # "websocket": AllowedHostsOriginValidator(
#     #             AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
#     #         ),
# })
