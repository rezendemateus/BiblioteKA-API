from .models import User
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, HistoricLoanSerializer
from .permissions import IsAccountAdminOrOwner
from copies.models import Loan
from rest_framework.generics import get_object_or_404


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountAdminOrOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"


class HistoricDetailView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountAdminOrOwner]

    serializer_class = HistoricLoanSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["user_id"])
        return Loan.objects.filter(user__id=user.id)
