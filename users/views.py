from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, OTPVerifySerializer, LoginSerializer
from .models import CustomUser, UserOTP
import random
from datetime import timedelta
from django.utils import timezone
from .emails import SendOTPEmail
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny



class RegisterAPI(APIView):
    
    def post(self, request):
        permission_classes = [AllowAny] 
        
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                
                # Saving user as inactive
                user = serializer.save(is_active=False)
                
                # Generating OTP
                otp = random.randint(100000, 999999)
                
                # Saves OTP in UserOTP with expiry
                UserOTP.objects.create(
                    user=user,
                    otp=otp,
                    otp_expires_at = timezone.now() + timedelta(minutes=5),
                )            
                
                # Sending OTP to email
                SendOTPEmail(user.email, "Your OTP for Registration to CollabSpace", f"Your OTP is {otp}. It is valid for 5 minutes.")

                # success response
                return Response({
                    "status": True,
                    "message": "User registered successfully. OTP sent to email.",
                    "data": {}
                })
                
            return Response({
                "status": False,
                "message": "Invalid data",
                "data": serializer.errors
            })
            
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        

class OTPVerifyAPI(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        
        try:
            serializer = OTPVerifySerializer(data=request.data)
            if serializer.is_valid():
                
                # user passed from serializer
                user = serializer.validated_data['user']
                
                # Acivate the user
                user.is_active = True
                user.save() # saving the user after activating
                
                # Delete OTP(s) for this user
                UserOTP.objects.filter(user=user).delete()
                
                return Response({
                    'status': True, 
                    'message': "OTP verified successfully. User activated.",
                    'data': {}
                })
                
            return Response({
                "status": False,
                "message": "Invalid OTP",
                "data": serializer.errors
            })
        
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        


class LoginAPI(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        
        try:
            serializer = LoginSerializer(data = request.data)
            
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                
                
                user = authenticate(email=email, password=password)
                
                if user is None:
                    
                    return Response({
                        "status": False, 
                        "message": "Invalid password",
                        "data": {}
                    })
                    
                if not user.is_active:
                    raise AuthenticationFailed("User is not active")
                
                # Refresh Token (JWT)
                refresh = RefreshToken.for_user(user)

                return Response({
                    'status': True,
                    'message': "Login successful",
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            
            
            return Response({
                "status": False, 
                "message": "Something went wrong",
                "data": serializer.errors
            })
                
                
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        