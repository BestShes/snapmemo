from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from memo.models import Category, Memo
from user.models import MemberCategory
from utils.customexception import ValidationException


class MemoSerializer(ModelSerializer):
    category_id = serializers.IntegerField(required=False, default=0)
    created_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    image = serializers.ImageField(allow_null=True)

    class Meta:
        model = Memo

        fields = (
            'id',
            'title',
            'content',
            'image',
            'category_id',
            'created_date',
            'modified_date',
        )

    def update(self, instance, validated_data):
        user = self.context['request'].user
        modify_image = validated_data.pop('image', instance.image)
        modify_content = validated_data.pop('content', '')
        category_id = validated_data.pop('category_id', instance.category_id)
        if user.categories.filter(id=category_id).exists():
            instance.content = modify_content
            instance.image = modify_image
            instance.category_id = category_id
            instance.save()
        else:
            raise ValidationException('해당 카테고리에 대한 권한이 없습니다.')
        return instance

    def create(self, validated_data):
        user = self.context['request'].user
        category_id = validated_data.pop('category_id', 0)
        if not user.categories.filter(id=category_id).exists():
            raise ValidationException('해당 카테고리에 대한 권한이 없습니다.')
        memo = Memo(user_id=user.id, category_id=category_id, **validated_data)
        memo.save()
        return memo


class CategorySerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=False)
    modify_title = serializers.CharField(max_length=100, write_only=True, required=False)
    memo_count = serializers.SerializerMethodField()
    created_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    modified_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Category

        fields = (
            'id',
            'title',
            'modify_title',
            'created_date',
            'modified_date',
            'memo_count'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data.pop('title', None)
        if title is None:
            raise ValidationException('Title을 입력해 주세요.')
        if user.categories.filter(title=title).exists():
            raise ValidationException('해당 디렉토리 명이 이미 존재합니다.')
        category = Category.objects.create(title=title)
        MemberCategory.objects.create(member=user, category=category)
        return category

    def update(self, instance, validated_data):
        modify_title = validated_data.pop('modify_title', None)
        if modify_title is None:
            raise ValidationException('변경할 Title을 입력 해 주세요.')
        instance.title = modify_title
        instance.save()
        return instance

    def get_memo_count(self, instance):
        return instance.memo_set.filter(user_id=self.context['request'].user.id).count()


class CategoryMemoNestedSerializer(CategorySerializer):
    memo = serializers.SerializerMethodField()

    class Meta:
        model = Category

        fields = (
            'id',
            'title',
            'modify_title',
            'created_date',
            'modified_date',
            'memo_count',
            'memo'
        )

    def get_memo(self, obj):
        user = self.context['request'].user
        data = obj.memo_set.filter(user_id=user.id)
        serializer = MemoSerializer(data, many=True)
        return serializer.data
