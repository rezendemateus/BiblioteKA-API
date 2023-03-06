from .models import User
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserView(CreateAPIView):
    pass


class UserDetailView(RetrieveUpdateDestroyAPIView):
    pass
