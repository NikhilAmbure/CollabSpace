import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from collab.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollabSpace.settings')
django.setup()

ws_pattern = [
    path("ws/chat/<int:workspace_id>/", ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handles normal HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(ws_pattern) # websocket routes
    ),
}) 

