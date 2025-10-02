from rest_framework import serializers
from .models import WorkSpace, Collaborator, ChatMessage, Invite, Notification, WorkSpaceMember
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
        

class WorkSpaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'owner', 'created_at']
        
        
class WorkSpaceMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    workspace = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = WorkSpaceMember
        fields = ['id', 'user', 'workspace', 'role', 'joined_at']
        

class InviteSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    workspace = serializers.StringRelatedField(read_only=True) # __str__ method of WorkSpace model
    
    class Meta:
        model = Invite
        fields = ['id', 'sender', 'receiver', 'workspace', 'status', 'created_at']
        

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    workspace = serializers.StringRelatedField(read_only=True) 
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'workspace', 'message', 'timestamp']
        
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
    