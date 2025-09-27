from django.db import models
from users.models import CustomUser


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="document")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)