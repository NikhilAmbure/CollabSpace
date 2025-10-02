from django.db import models
from _docs.models import Document
from django.conf import settings

User = settings.AUTH_USER_MODEL


# For document collaboration
class Collaborator(models.Model):
    ROLE_CHOICES = (("editor", "Editor"), ("viewer", "Viewer"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="collaborators")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.user} as {self.role} of {self.document}"
    
 
#  workspae collaboration
class WorkSpace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workspaces_created")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class WorkSpaceMember(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
    ]
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workspaces_memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)
    
    # a user can't join the same workspace twice
    class Meta:
        unique_together = ("workspace", "user") 
    
    def __str__(self):
        return f"{self.user} in {self.workspace} ({self.role})"
    
    
class Invite(models.Model):
     STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
    ]
     
     workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="invites")
     invited_user_email = models.EmailField()
     invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invites_sent")
     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
     created_at = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
         return f"Invite to {self.invited_user_email} for {self.workspace} ({self.status})"
     
     
class ChatMessage(models.Model):
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_messages_sent")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender} in {self.workspace}: {self.message[:30]}"
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user}: {self.message[:30]}"

