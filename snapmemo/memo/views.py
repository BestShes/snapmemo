from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from memo.models import Category, Memo
from memo.serializers import CategorySerializer, MemoSerializer, CategoryMemoNestedSerializer
from utils import CategoryPermission, MemoPermission
from utils.customexception import ValidationException


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'
    permission_classes = (CategoryPermission,)

    def get_serializer_class(self):
        action = self.action
        user_agent = self.request.META['HTTP_USER_AGENT']
        if (user_agent.find('iPhone') != -1 or user_agent.find('iPad') != -1) or action == 'retrieve':
            return CategoryMemoNestedSerializer
        else:
            return self.serializer_class

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = Category.objects.filter(member=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.id == 0:
            raise ValidationException('기본 폴더는 삭제 할 수 없습니다.')
        else:
            instance.delete()


class MemoViewSet(ModelViewSet):
    serializer_class = MemoSerializer
    queryset = Memo.objects.all()
    lookup_field = 'id'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'content')
    permission_classes = (MemoPermission,)

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        list_queryset = Memo.objects.filter(user_id=user_id)
        queryset = self.filter_queryset(list_queryset).order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={
            'memo': serializer.data,
        }, status=status.HTTP_201_CREATED, headers=headers)
