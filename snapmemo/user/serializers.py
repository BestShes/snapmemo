from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import Member
from utils import customexception
from utils.validation import CheckSocialAccessToken


class UserViewSetSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(max_length=50, required=True)
    password = serializers.CharField(min_length=8, required=False, write_only=True)
    access_key = serializers.CharField(required=False, write_only=True)
    current_password = serializers.CharField(min_length=8, required=False, write_only=True)
    modify_password = serializers.CharField(min_length=8, required=False, write_only=True)

    class Meta:
        model = Member
        fields = (
            'id',
            'username',
            'password',
            'user_type',
            'access_key',
            'created_date',
            'current_password',
            'modify_password'
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

    def update(self, instance, validated_data):
        current_password = validated_data['current_password']
        modify_password = validated_data['modify_password']
        user_object = authenticate(username=instance.username, password=current_password)
        if user_object is None:
            raise customexception.ValidationException('패스워드가 정확하지 않습니다')
        else:
            user_object.set_password(modify_password)
            user_object.save()
        return user_object


class FacebookUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=260, required=False)
    password = serializers.CharField(required=False, write_only=True)
    access_key = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Member
        fields = (
            'id',
            'username',
            'password',
            'user_type',
            'access_key',
            'created_date',
        )

    def create(self, validated_data):
        access_token = validated_data['access_key']
        username = CheckSocialAccessToken.check_facebook(access_token)
        user_object = Member(username=username, **validated_data)
        user_object.save()
        return user_object




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
