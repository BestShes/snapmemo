from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from user.models import Member
from user.serializer import UserViewSetSerializer


class UserViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = UserViewSetSerializer
    lookup_field = 'username'
    permission_classes = (permissions.AllowAny,)
