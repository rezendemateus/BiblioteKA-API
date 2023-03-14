from .models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from copies.models import Loan
from copies.serializers import LoanSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_superuser",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
            },
            "email": {
                "validators": [UniqueValidator(queryset=User.objects.all())],
            },
        }

    def create(self, validated_data: dict) -> User:
        if validated_data.get("is_superuser", None):
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance


class HistoricLoanSerializer(LoanSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "borrowed_at",
            "loan_term_at",
            "amount_paid",
            "paid_at",
            "book_name",
        ]
