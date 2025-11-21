from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    PasswordChangeSerializer
)
from .models import User
from quiz_management.utils import success_response, error_response


class UserRegistrationView(APIView):
    """
    Register a new admin user.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new admin user",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response('User created successfully', UserSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return success_response(
                data=user_data,
                message="User registered successfully",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Registration failed",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    """
    Login user and return JWT tokens.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Login user and get JWT tokens",
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                'Login successful',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return success_response(
                data={
                    'user': UserSerializer(user).data,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                },
                message="Login successful"
            )
        return error_response(
            message="Login failed",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class UserLogoutView(APIView):
    """
    Logout user by blacklisting the refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout user by blacklisting refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: 'Logout successful',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return error_response(
                    message="Refresh token is required",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return success_response(message="Logout successful")
        except Exception as e:
            return error_response(
                message="Logout failed",
                details=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    """
    Get or update user profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={200: UserSerializer}
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response(data=serializer.data, message="Profile retrieved successfully")

    @swagger_auto_schema(
        operation_description="Update user profile",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: 'Bad Request'
        }
    )
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Profile updated successfully")
        return error_response(
            message="Profile update failed",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class PasswordChangeView(APIView):
    """
    Change user password.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change user password",
        request_body=PasswordChangeSerializer,
        responses={
            200: 'Password changed successfully',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            
            return success_response(message="Password changed successfully")
        return error_response(
            message="Password change failed",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
