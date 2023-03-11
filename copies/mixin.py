from django.shortcuts import get_object_or_404
from users.models import User
from copies.models import Loan
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import PermissionDenied
from books.models import Book
from datetime import datetime


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

        return super().post(request, *args, **kwargs)


class VerifyFollowersAndDayToTermMixin:
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs["book_id"])
        loan_date = datetime.now()
        loan_termin_at = loan_date + timedelta(days=7)

        if book.followers.count() > 10:
            loan_termin_at = loan_date + timedelta(days=4)
        if loan_termin_at.strftime("%A") == "Saturday":
            loan_termin_at = loan_termin_at + timedelta(days=2)
        if loan_termin_at.strftime("%A") == "Sunday":
            loan_termin_at = loan_termin_at + timedelta(days=1)

        request.data["loan_term_at"] = loan_termin_at

        return super().post(request, *args, **kwargs)
