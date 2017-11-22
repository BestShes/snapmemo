from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from memo.models import Category
from user.models import Member, MemberCategory
from utils import customexception
from utils.validation import CheckSocialAccessToken


class UserViewSetSerializer(serializers.ModelSerializer):
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

        extra_kwargs = {
            'username': {'max_length': 50, 'required': True,
                         'validators': [UniqueValidator(queryset=Member.objects.all())]},
            'password': {'min_length': 8, 'required': True, 'write_only': True},
            'access_key': {'required': False, 'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('type', None)
        super(UserViewSetSerializer, self).__init__(*args, **kwargs)

        if user_type == 'facebook':
            extra_kwargs = self.Meta.extra_kwargs
            extra_kwargs['username']['required'] = False
            extra_kwargs['password']['required'] = False
            extra_kwargs['access_key']['required'] = True

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        access_key = validated_data.pop('access_key', None)
        default_category = Category.objects.get(id=0)
        if access_key is None:
            user_object = Member(**validated_data)
            user_object.set_password(password)
            user_object.save()
        elif password is None:
            username = CheckSocialAccessToken.check_facebook(access_key)
            if Member.objects.filter(username=username).exists():
                raise customexception.ValidationException('이미 존재하는 계정입니다.')
            user_object = Member(username=username, **validated_data)
            user_object.save()
        MemberCategory.objects.create(member=user_object, category=default_category)
        return user_object

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


class NormalUserLoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True, max_length=50)
    password = serializers.CharField(min_length=8, write_only=True, required=True)

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


class SocialUserLoginSerializer(serializers.Serializer):
    access_key = serializers.CharField(max_length=260, write_only=True, required=True)

    class Meta:
        fields = (
            'access_key',
        )

    def create(self, validated_data):
        access_key = validated_data['access_key']
        username = CheckSocialAccessToken.check_facebook(access_key)
        user_object = Member.objects.get(username=username)
        return user_object
