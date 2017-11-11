from rest_framework.permissions import BasePermission

__all__ = (
    'UserPermission',
    'CategoryPermission',
    'MemoPermission'
)


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated() and request.user.is_superuser
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and (obj == request.user or request.user.is_superuser)
        else:
            return False


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and (request.user in obj.member_set.all() or request.user.is_superuser)
        else:
            return False


class MemoPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and (request.user == obj.user or request.user.is_superuser)
        else:
            return False
