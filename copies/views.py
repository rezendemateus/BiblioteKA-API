from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    UpdateAPIView,
)
from .models import Loan, Copy
from books.models import Book
from users.models import User
from .serializers import LoanSerializer
from books.permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ParseError, NotFound
from .permissions import IsUserUnblocked


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
        loan = Loan.objects.filter(id=self.kwargs.get("loan_id")).first()
        if not loan:
            raise NotFound("Loan does not exist")

        return loan
