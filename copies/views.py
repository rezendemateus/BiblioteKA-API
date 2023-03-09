from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    UpdateAPIView
    )
from .models import Loan, Copy
from books.models import Book
from users.models import User
from .serializers import LoanSerializer
from books.permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ParseError


class LoanView(CreateAPIView):
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

        serializer.save(copy=copy, user=user)


class LoanDetailView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_update(self, serializer):
        copy = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        user = get_object_or_404(User, pk=self.kwargs.get(user.id))

        serializer.save(copy=copy, user=user)
