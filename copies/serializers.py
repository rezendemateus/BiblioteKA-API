from rest_framework import serializers
from models import Loan
from datetime import timezone


class LoanSerializer(serializers.ModelSerializer):
    amount_paid = serializers.IntegerField(allow_null=True)
    paid_at = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = Loan
        fields = [
            "amount_paid",
            "barrowed_at",
            "copy_id",
            "loan_term_at",
            "paid_at",
            "user_id"
            ]
        read_only_fields = ["borrowed_at"]

    def create(self, validated_data):
        loan_date = timezone.now()
        self.loan_term_at = loan_date + timezone.timedelta(days=7)

        return Loan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.paid_at = timezone.now()
        instance.save()

        return instance
