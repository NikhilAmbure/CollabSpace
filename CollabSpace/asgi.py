import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CollabSpace.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import collab.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handles normal HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(collab.routing.websocket_urlpatterns) # websocket routes
    ),
}) 

