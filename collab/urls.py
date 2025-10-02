from rest_framework.routers import DefaultRouter
from .views import (
    WorkSpaceViewSet, 
    WorkSpaceMemberViewSet, 
    InviteViewSet, 
    ChatMessageViewSet, 
    NotificationViewSet
)

router = DefaultRouter()
router.register(r'workspaces', WorkSpaceViewSet, basename='workspace')
router.register(r'members', WorkSpaceMemberViewSet, basename='member')
router.register(r'invites', InviteViewSet, basename='invite')
router.register(r'chat', ChatMessageViewSet, basename='chat')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls