from rest_framework import serializers
from .models import Loan
from datetime import timedelta, datetime
from django.utils import timezone
import ipdb


class LoanSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    book_name = serializers.SerializerMethodField()
    loan_term = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "amount_paid",
            "borrowed_at",
            "copy_id",
            "loan_term_at",
            "paid_at",
            "user_id",
            "username",
            "book_name",
            "loan_term"
            ]
        read_only_fields = [
            "username",
            "user_id",
            "copy_id",
            # "loan_term_at",
            "book_name",
            "loan_term",
            ]
        extra_kwargs = {
            "paid_at": {
                "allow_null": True,
                "default": None
                },
            "loan_term_at": {
                "write_only": True
            }
            }

    def get_username(self, object):
        return object.user.username

    def get_user_id(self, object):
        return object.user.id

    def get_book_name(self, object):
        return object.copy.book.title

    def get_loan_term(self, object):
        return self.loan_term_at.strftime("%A, %d, %b, %Y")

    def create(self, validated_data):
        loan_date = datetime.now()
        loan_termin_at = loan_date + timedelta(days=7)

        if loan_termin_at.strftime("%A") == "Saturday":
            loan_termin_at = (loan_termin_at + timedelta(days=2))
        if loan_termin_at.strftime("%A") == "Sunday":
            loan_termin_at = (loan_termin_at + timedelta(days=1))

        validated_data["loan_term_at"] = loan_termin_at
        # loan = Loan(validated_data, {"loan_term_at": loan.termin_at})
        # loan.save()
        # return Loan.objects.create(**validated_data)
        return Loan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.paid_at = timezone.now()
        instance.save()

        return instance
