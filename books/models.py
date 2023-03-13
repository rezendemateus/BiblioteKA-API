from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    synopsis = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=100)
    published_at = models.DateField()

    followers = models.ManyToManyField(
        "users.User",
        through="books.Follower",
        related_name="books",
    )

    genders = models.ManyToManyField("books.Gender", related_name="books")

    avaliations = models.ManyToManyField(
        "users.User",
        through="books.Avaliation",
        related_name="book_list",
    )


class Follower(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)


class Gender(models.Model):
    name = models.CharField(
        max_length=150,
    )


class StarChoices(models.TextChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Avaliation(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    satisfaction_stars = models.CharField(max_length=1, choices=StarChoices.choices)
