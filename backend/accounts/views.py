# accounts.views.py

from typing import Any, Optional

from django.conf import settings
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.users import User
from accounts.renderers import UserJSONRenderer
from accounts.serializers import (
    LogoutSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class UserRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request) -> Response:
        """
        Return user response after a successful registration.
        """
        user_request = request.data.get('user', {})
        serializer = self.serializer_class(data=user_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


user_register_view = UserRegistrationAPIView.as_view()


class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserLoginSerializer

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


user_login_view = UserLoginAPIView.as_view()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Return user on GET request.
        """
        serializer = self.serializer_class(
            request.user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Return updated user.
        """
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


user_retrieve_view = UserRetrieveUpdateAPIView.as_view()


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """
        Validate token and save.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


logout_view = LogoutAPIView.as_view()
