from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadOnly
from .models import Book
from .serializer import BookSerializer, BookDetailSerializer
from django.shortcuts import get_object_or_404
from copies.models import Copy
from rest_framework.views import Request, Response, status


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

    def update(self, request: Request, *args, **kwargs) -> Book:
        book_id = kwargs["book_id"]
        book_obj: Book = get_object_or_404(Book, id=book_id)

        serializer = BookDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data["copies"] >= 0:
            copies_list_obj = [
                Copy(book=book_obj) for _ in range(serializer.data["copies"])
            ]

            Copy.objects.bulk_create(copies_list_obj)

        if serializer.data["copies"] < 0:
            for delete_copy in range(serializer.data["copies"] * -1):
                delete_copy = Copy.objects.filter(book=book_obj, avaliable=True).first()

                if not delete_copy:
                    serializer = BookSerializer(book_obj)
                    return Response(serializer.data)

                delete_copy.delete()

        serializer = BookSerializer(book_obj)

        return Response(serializer.data)

    def destroy(self, request: Request, *args, **kwargs):
        book_id = kwargs["book_id"]
        book_obj: Book = get_object_or_404(Book, id=book_id)

        borrowed_copy = book_obj.copies.filter(avaliable=False).first()

        if borrowed_copy:
            return Response(
                data={"message": "Unable to delete a book with a borrowed copy"},
                status=409,
            )

        book_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
