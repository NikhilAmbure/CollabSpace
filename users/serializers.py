from rest_framework import serializers
from .models import CustomUser, UserOTP
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")
        return username
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email
        
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
            is_active = False  # Keeping inactive until OTP is verified
        )
        
        user.set_password(validated_data['password']) # hash password
        user.save()
        return user

        

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    
    def validate(self, data):

        # get user by email
        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        
        
        # checking if OTP is exists for this user
        if not UserOTP.objects.filter(user=user, otp=data['otp'], otp_expires_at__gt=timezone.now()).exists():
            raise serializers.ValidationError("Invalid or expired OTP")
        
        # Passing user
        data['user'] = user
        return data