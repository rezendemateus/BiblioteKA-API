from django.shortcuts import get_object_or_404
from users.models import User
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied


class VerifyIfUserIsBlockedMixin:
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data["username"])
        if user.blocked_until:
            isBlockedYet = (user.blocked_until - timezone.now()).days

            if isBlockedYet >= 0:
                raise PermissionDenied(
                    f"User is blocked until: {user.blocked_until.strftime('%d/%b/%Y')}!"
                )
            user.blocked_until = None
            user.save()

        return super().create(request, *args, **kwargs)
