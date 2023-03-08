from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadOnly, IsFollowerOwner
from .models import Book, Follower
from .serializer import BookSerializer, FollowerSerializer


class BooksView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BooksDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    lookup_url_kwarg = "book_id"
    ...


class FollowerView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FollowerSerializer

    def get_queryset(self):
        try:
            book_obj = Book.objects.get(pk=self.kwargs["books_id"])
        except Book.DoesNotExist:
            raise NotFound("Book does not exists!")

        follower_queryset = Follower.objects.filter(
            book_id=book_obj.id,
            user_id=self.request.user.id,
        )

        return follower_queryset

    def perform_create(self, serializer):
        try:
            book_obj = Book.objects.get(pk=self.kwargs["books_id"])
        except Book.DoesNotExist:
            raise NotFound("Book does not exists!")

        is_follower = Follower.objects.filter(
            book_id=book_obj.id, user_id=self.request.user.id
        ).first()
        if is_follower:
            raise ParseError("You already follow this book.")

        serializer.save(book=book_obj, user=self.request.user)


class FollowerDetailView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFollowerOwner]

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    lookup_url_kwarg = "follower_id"

    def get_queryset(self):
        try:
            book_obj = Book.objects.get(pk=self.kwargs["books_id"])
        except Book.DoesNotExist:
            raise NotFound("Book does not exists!")

        follower_queryset = Follower.objects.filter(book_id=book_obj.id)

        return follower_queryset
