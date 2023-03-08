from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadOnly
from .models import Book
from .serializer import BookSerializer
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

        add_copies = request.data.pop("add_copies", None)
        delete_copies = request.data.pop("delete_copies", None)

        if add_copies:
            copies_list_obj = [Copy(book=book_obj) for _ in range(add_copies)]

            Copy.objects.bulk_create(copies_list_obj)

        if delete_copies:
            for delete_copy in range(delete_copies):
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
