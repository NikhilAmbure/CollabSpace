from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)


class UserOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.email} - {self.otp}"