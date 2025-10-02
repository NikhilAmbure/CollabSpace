from django.shortcuts import render
from rest_framework import viewsets, status
from .models import WorkSpace, Collaborator, ChatMessage, Invite, Notification, WorkSpaceMember
from .serializers import (
    WorkSpaceSerializer,
    ChatMessageSerializer, 
    InviteSerializer, 
    NotificationSerializer, 
    WorkSpaceMemberSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class WorkSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Return only workspaces the user is a member of"""
        return WorkSpace.objects.filter(member__user=self.request.user)
    

    @action(detail=True, methods=["post"])
    def invite(self, request, pk=None):
        """Inviting user to a workspace"""
        workspace = self.get_object()
        receiver_id = request.data.get("receiver_id")

        invite = Invite.objects.create(
            workspace=workspace,
            sender=request.user,
            receiver_id=receiver_id,
            status="pending"
        )

        return Response(InviteSerializer(invite).data, status=status.HTTP_201_CREATED)
    

class WorkSpaceMemberViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSpaceMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkSpaceMember.objects.filter(workspace__members__user=self.request.user)


class InviteViewSet(viewsets.ModelViewSet):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invite.objects.filter(receiver=self.request.user)


    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        """Accept an invite"""
        invite = self.get_object()
        invite.status = "accepted"
        invite.save()

        # Adding receiver to workspace members
        WorkSpaceMember.objects.create(
            workspace=invite.workspace,
            user = invite.receiver,
            role = "member"
        )

        return Response({
            "status": True,
            "message": "Invite Accepted."
        })
    
    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        """"Decline an invite"""
        invite = self.get_object()
        invite.status = 'declined'
        invite.save()
        return Response({
            "status": True,
            "message": "Invite Declined."
        })
    

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(workspace__members__user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({
            "status": True,
            "message": "Notification marked as read"
        })