from rest_framework import serializers
from .models import Loan
from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework.exceptions import ParseError
from books.models import StarChoices
from books.models import Avaliation


class LoanSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", write_only=True)
    book_name = serializers.CharField(source="copy.book.title", read_only=True)
    user = serializers.SerializerMethodField()
    satisfaction_stars = serializers.ChoiceField(
        choices=StarChoices.choices,
        default=None,
    )

    class Meta:
        model = Loan
        fields = [
            "id",
            "borrowed_at",
            "loan_term_at",
            "amount_paid",
            "paid_at",
            "book_name",
            "user",
            "username",
            "satisfaction_stars",
        ]
        read_only_fields = [
            "username",
            "user_id",
            "copy_id",
        ]
        extra_kwargs = {"paid_at": {"allow_null": True, "default": None}}

    def get_user(self, object):
        user = {"id": object.user.id, "username": object.user.username}
        return user

    def create(self, validated_data: dict):
        if validated_data.get("satisfaction_stars", False) is not False:
            validated_data.pop("satisfaction_stars")
        return super().create(validated_data)

    def update(self, instance: Loan, validated_data: dict):
        if instance.paid_at:
            raise ParseError("book has already been returned!")

        instance.amount_paid = calculate_loan_amount(instance.loan_term_at)
        instance.paid_at = timezone.now()
        instance.copy.avaliable = True
        instance.copy.save()
        instance.save()
        if instance.amount_paid > 0:
            instance.user.blocked_until = timezone.now() + timedelta(days=7)
            instance.user.save()

        instance.satisfaction_stars = None
        if validated_data.get("satisfaction_stars"):
            avaliation_obj = Avaliation.objects.filter(
                user=instance.user, book=instance.copy.book
            ).first()
            if avaliation_obj:
                avaliation_obj.satisfaction_stars = validated_data["satisfaction_stars"]
                avaliation_obj.save()
            else:
                avaliation_obj = Avaliation.objects.create(
                    user=instance.user,
                    book=instance.copy.book,
                    satisfaction_stars=validated_data["satisfaction_stars"],
                )
            instance.satisfaction_stars = avaliation_obj.satisfaction_stars

        return instance


def calculate_loan_amount(loan_terminated_date: datetime):
    today = timezone.now()
    loan_terminated = loan_terminated_date

    days = (today - loan_terminated).days

    if days <= 0:
        return 0

    total = 5 + (days * 0.5)

    return total
