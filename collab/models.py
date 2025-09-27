from django.db import models
from users.models import CustomUser
from _docs.models import Document


class Collaborator(models.Model):
    ROLE_CHOICES = (("editor", "Editor"), ("viewer", "Viewer"))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="collaborators")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    