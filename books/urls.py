from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BooksView.as_view()),
    path("books/<int:book_id>/", views.BooksDetailView.as_view()),
    path("books/<int:books_id>/follower/", views.FollowerView.as_view()),
    path(
        "books/<int:books_id>/follower/<int:follower_id>/",
        views.FollowerDetailView.as_view(),
    ),
]
