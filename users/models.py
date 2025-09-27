from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
