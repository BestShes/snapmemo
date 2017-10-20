from rest_framework.permissions import BasePermission

__all__ = (
    'UserPermission',
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
