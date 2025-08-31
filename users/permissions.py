from rest_framework import permissions

from users.models import User


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and not request.user.is_superuser


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj.email == request.user.email
        elif hasattr(obj, "owner"):
            return obj.owner == request.user
        return False
