from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import Member
from utils import customexception


class UserViewSetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=False, write_only=True)
    access_key = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Member
        fields = (
            'username',
            'password',
            'user_type',
            'access_key',
            'created_date',
        )

    def create(self, validated_data):
        user = Member(**validated_data)
        try:
            password = validated_data.pop('password')
            user.set_password(password)
        except KeyError:
            pass
        user.save()
        return user


class NormalUserLoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        fields = (
            'username',
            'password'
        )

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user_object = authenticate(username=username, password=password)
        if user_object is None:
            raise customexception.AuthenticateException('이메일 혹은 비밀번호를 확인해 주세요.')
        return user_object


class UserLogoutSerializer(serializers.Serializer):
    pass
