from rest_framework.urls import path
from .views import LoanDetailView, LoanView

urlpatterns = [
    path("books/<int:book_id>/loan/", LoanView.as_view()),
    path("books/loan/<int:loan_id>/", LoanDetailView.as_view()),
]
