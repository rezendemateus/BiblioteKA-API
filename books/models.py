from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    synopsis = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=100)
    published_at = models.DateField()

    folowers = models.ManyToManyField(
        "users.User",
        through="books.Folower",
        related_name="books",
    )

    genders = models.ManyToManyField(
        "books.Gender",
        related_name="books",
    )


class Folower(models.Model):
    book_id = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE)


class Gender(models.Model):
    name = models.CharField(
        max_length=150,
    )
