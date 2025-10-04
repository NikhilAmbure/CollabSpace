from django.urls import re_path
from collab.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<workspace_id>\w+)/$", ChatConsumer.as_asgi()),
]