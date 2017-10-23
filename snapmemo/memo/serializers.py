from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from memo.models import Category, Memo
from utils.customexception import ValidationException


class MemoSerializer(ModelSerializer):
    category_id = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = Memo

        fields = (
            'id',
            'title',
            'content',
            'image',
            'category_id'
        )

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        memo = Memo(user_id=user_id, **validated_data)
        memo.save()
        return memo


class CategorySerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=False)
    modify_title = serializers.CharField(max_length=100, write_only=True, required=False)
    memo = MemoSerializer(many=True, read_only=True, source='memo_set')

    class Meta:
        model = Category

        fields = (
            'id',
            'title',
            'modify_title',
            'memo'
        )

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        try:
            title = validated_data['title']
        except KeyError:
            raise ValidationException('title을 입력 해 주세요')
        if Category.objects.filter(user_id=user_id, title=title).exists():
            raise ValidationException('해당 디렉토리 명이 이미 존재합니다.')
        category = Category(user_id=user_id, **validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        try:
            modify_title = validated_data['modify_title']
        except KeyError:
            raise ValidationException('변경할 Title을 입력 해 주세요.')
        instance.title = modify_title
        instance.save()
        return instance
