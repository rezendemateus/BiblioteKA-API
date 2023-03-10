from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from users.models import User
from rest_framework.views import View
from books.models import Follower


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.method in SAFE_METHODS or request.user.is_superuser


class IsFollowerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Follower):
        return request.user.is_authenticated and obj.user.id == request.user.id
