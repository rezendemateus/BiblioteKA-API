from rest_framework import serializers
from .models import Loan
from datetime import timedelta, datetime
from django.utils import timezone


class LoanSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", write_only=True)
    book_name = serializers.CharField(source="copy.book.title", read_only=True)
    loan_term = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "id",
            "loan_term",
            "amount_paid",
            "borrowed_at",
            "paid_at",
            "book_name",
            "user",
            "username",
        ]
        read_only_fields = [
            "username",
            "user_id",
            "copy_id",
            "book_name",
            "loan_term",
        ]
        extra_kwargs = {"paid_at": {"allow_null": True, "default": None}}

    def get_loan_term(self, object):
        return object.loan_term_at.strftime("%A, %d, %b, %Y")

    def get_user(self, object):
        user = {"id": object.user.id, "username": object.user.username}
        return user

    def create(self, validated_data):
        loan_date = datetime.now()
        loan_termin_at = loan_date + timedelta(days=7)

        if loan_termin_at.strftime("%A") == "Saturday":
            loan_termin_at = loan_termin_at + timedelta(days=2)
        if loan_termin_at.strftime("%A") == "Sunday":
            loan_termin_at = loan_termin_at + timedelta(days=1)
        validated_data["loan_term_at"] = loan_termin_at

        return Loan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount_paid = calculate_loan_amount(instance.loan_term_at)
        instance.paid_at = timezone.now()
        instance.copy.available = True
        instance.copy.save()
        instance.save()

        return instance


def calculate_loan_amount(loan_terminated_date: datetime):
    today = timezone.now()
    loan_terminated = loan_terminated_date

    days = (today - loan_terminated).days

    if days <= 0:
        return 0

    total = 5 + (days * 0.5)

    return total
