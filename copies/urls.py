from rest_framework.urls import path
from views import LoanDetailView

urlpatterns = [
    path("/books/<int:books_id>/loan/", LoanDetailView.as_view())
]
