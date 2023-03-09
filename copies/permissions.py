from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
import ipdb


class IsUserUnblocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return not get_object_or_404(
            User, username=request.data["username"]
        ).blocked_until
