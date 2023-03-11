from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404, CreateAPIView, UpdateAPIView
from rest_framework.exceptions import ParseError, NotFound
from .mixin import VerifyIfUserIsBlockedOrHavePendingBooksMixin
from .models import Loan, Copy
from books.models import Book
from users.models import User
from .serializers import LoanSerializer
from books.permissions import IsAdminOrReadOnly
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import schedule
import time


class LoanView(VerifyIfUserIsBlockedOrHavePendingBooksMixin, CreateAPIView):
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

        if copy is True:
            return send_mail(
                subject="Um livro que você segue está disponível!",
                message="Olá, vimos que você segue o livro"
                f' "{loan.copy.book.title}" '
                "e gostaríamos de avisar que ele já está disponível para retirada!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers,
                fail_silently=False,
            )

        return loan


def reminder_devolution():
    loans = Loan.objects.all()

    for loan in loans:
        reminder_day = loan.loan_term_at - timedelta(days=1)
        user_email = loan.user.email

        if reminder_day is loan.loan_term_at - timedelta(days=1):
            send_mail(
                subject="ATENÇÃO: Lembrete de devolução!",
                message="O livro que você emprestou"
                f' "{loan.copy.book.title}" '
                "deve ser devolvido até amanhã! Lembre-se: há taxa de multa caso não seja devolvido no dia, e esse valor é atualizado diariamente! Caso precise de mais tempo, renove seu empréstimo!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=False,
            )


schedule.every().day.at("10:00").do(reminder_devolution)

while True:
    schedule.run_pending()
    time.sleep(1)
