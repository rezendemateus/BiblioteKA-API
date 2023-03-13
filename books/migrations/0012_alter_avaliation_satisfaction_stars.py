# Generated by Django 4.1.7 on 2023-03-12 00:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0011_avaliation_book_avaliations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avaliation",
            name="satisfaction_stars",
            field=models.CharField(
                choices=[
                    ("1", "One"),
                    ("2", "Two"),
                    ("3", "Three"),
                    ("4", "Four"),
                    ("5", "Five"),
                ],
                max_length=1,
                null=True,
            ),
        ),
    ]