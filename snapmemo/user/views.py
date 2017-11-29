from rest_auth.app_settings import create_token
from rest_auth.models import TokenModel
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.models import Member
from user.serializers import UserViewSetSerializer, UserLoginSerializer
from utils import UserPermission


class UserViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = UserViewSetSerializer
    lookup_field = 'id'
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        action = self.action
        if action == 'login':
            return UserLoginSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        user_object = serializer.save()
        token = create_token(TokenModel, user_object, UserViewSetSerializer)
        return user_object, token

    def create(self, request, *args, **kwargs):
        user_type = request.data.get('user_type', 'normal')
        serializer = self.get_serializer(data=request.data, user_type=user_type)
        serializer.is_valid(raise_exception=True)
        _, token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={
            'user': serializer.data,
            'token': str(token)
        }, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        user_type = request.data.get('user_type', 'normal')
        serializer = self.get_serializer(data=request.data, user_type=user_type)
        serializer.is_valid(raise_exception=True)
        user_object, token = self.perform_create(serializer)
        user = UserViewSetSerializer(user_object, user_type=user_type)
        headers = self.get_success_headers(serializer.data)
        return Response(data={
            'user': user.data,
            'token': str(token)
        }, status=status.HTTP_200_OK, headers=headers)

    @list_route(methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        username = request.user.id
        user_token = TokenModel.objects.get(user_id=username)
        user_token.delete()
        return Response(data={'detail': 'Logout Succeeded and Token Delete'}, status=status.HTTP_200_OK)
