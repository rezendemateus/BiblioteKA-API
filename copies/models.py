from django.db import models


class Copy(models.Model):
    avaliable = models.BooleanField(default=True)
    book = models.ForeignKey(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="copies",
    )

    borrowed_to_users = models.ManyToManyField(
        "users.User", through="copies.Loan", related_name="copies"
    )


class Loan(models.Model):
    borrowed_at = models.DateTimeField(auto_now_add=True)
    loan_term_at = models.DateTimeField()
    amount_paid = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    paid_at = models.DateTimeField(null=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    copy = models.ForeignKey("copies.Copy", on_delete=models.CASCADE)
