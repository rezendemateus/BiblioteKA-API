from rest_framework.generics import ListCreateAPIView, get_object_or_404
from models import Loan, Copy
from users.models import User
from serializers import LoanSerializer


class LoanDetailView(ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy = get_object_or_404(Copy, pk=self.kwargs.get("book_id"))
        user = get_object_or_404(User, pk=self.kwargs.get(user.id))

        serializer.save(copy_id=copy, user_id=user)