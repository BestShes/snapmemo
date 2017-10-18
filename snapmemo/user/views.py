from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from rest_framework import permissions
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from user.models import Member
from user.serializers import UserViewSetSerializer, NormalUserLoginSerializer


class UserViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = UserViewSetSerializer
    lookup_field = 'username'
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        token = create_token(TokenModel, user, UserViewSetSerializer)
        return token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={
            'user': serializer.data,
            'token': str(token)
        }, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginViewSet(CreateModelMixin,
                       GenericViewSet):
    queryset = Member.objects.all()
    serializer_class = NormalUserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        token = create_token(TokenModel, user, NormalUserLoginSerializer)
        return token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={
            'user': serializer.data,
            'token': str(token)
        }, status=status.HTTP_200_OK, headers=headers)
