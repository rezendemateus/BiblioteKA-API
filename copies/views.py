from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404, CreateAPIView, UpdateAPIView
from rest_framework.exceptions import ParseError, NotFound
from .models import Loan, Copy
from books.models import Book
from users.models import User
from .serializers import LoanSerializer
from books.permissions import IsAdminOrReadOnly
from .mixin import (
    VerifyIfUserIsBlockedOrHavePendingBooksMixin,
    VerifyFollowersAndDayToTermMixin,
)
from django.core.mail import send_mail
from django.conf import settings
import copies.reminder_devolution  # não apagar


class LoanView(
    VerifyIfUserIsBlockedOrHavePendingBooksMixin,
    VerifyFollowersAndDayToTermMixin,
    CreateAPIView,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        user = get_object_or_404(User, username=self.request.data["username"])
        copy = Copy.objects.filter(book=book, avaliable=True).first()

        if not copy:
            raise ParseError("Copies unavailable")

        copy.avaliable = False
        copy.save()

        serializer.save(copy=copy, user=user)


class LoanDetailView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_url_kwarg = "loan_id"

    def get_object(self):
        loan = Loan.objects.filter(id=self.kwargs.get("loan_id")).first()
        followers = loan.copy.book.followers.all()
        followers = [follower.email for follower in followers]
        copy = loan.copy.avaliable

        if not loan:
            raise NotFound("Loan does not exist")

        if copy is False:
            send_mail(
                subject="Um livro que você segue está disponível!",
                message="Olá, vimos que você segue o livro"
                f' "{loan.copy.book.title}" '
                "e gostaríamos de avisar que ele já está disponível para retirada!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers,
                fail_silently=False,
            )

        return loan
