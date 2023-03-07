from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from users.models import User
from rest_framework.views import View


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.method in SAFE_METHODS or request.user.is_superuser
