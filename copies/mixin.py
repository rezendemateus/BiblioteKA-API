from django.shortcuts import get_object_or_404
from users.models import User
from copies.models import Loan
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import PermissionDenied


class VerifyIfUserIsBlockedOrHavePendingBooksMixin:
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

        isBorrowedBook = Loan.objects.filter(
            user=user, loan_term_at__lte=timezone.now()
        )
        if isBorrowedBook:
            user.blocked_until = timezone.now() + timedelta(days=7)
            user.save()
            raise PermissionDenied(
                f"You have {isBorrowedBook.count()} books to return!"
            )

        return super().create(request, *args, **kwargs)
