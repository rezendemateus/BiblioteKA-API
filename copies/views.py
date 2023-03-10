from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    UpdateAPIView,
)
from .models import Loan, Copy
from books.models import Book, Follower
from users.models import User
from .serializers import LoanSerializer
from books.permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ParseError, NotFound
from .permissions import IsUserUnblocked
from django.core.mail import send_mail
from django.conf import settings


class LoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsUserUnblocked]

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
        # import ipdb

        loan = Loan.objects.filter(id=self.kwargs.get("loan_id")).first()
        followers = loan.copy.book.followers.all()
        followers = [follower.email for follower in followers]
        copy = loan.copy.avaliable

        # ipdb.set_trace()

        if not loan:
            raise NotFound("Loan does not exist")

        print(copy is True, "---------------------------->")
        if copy is True:
            send_mail(
                subject="Teste de envio de email",
                message="Não foi um fracasso",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=followers,
                fail_silently=False,
            )
            print("Email enviado")

        return loan
