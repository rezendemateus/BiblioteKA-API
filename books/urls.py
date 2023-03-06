from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BooksView.as_view()),
    # path("books/:books_id/", .as_view()),
    # path("books/:books_id/follow/", .as_view()),
    # path("books/:books_id/loan/", .as_view()),
    # path("books/loan/:loan_id/", .as_view()),
]
