# Generated by Django 4.1.7 on 2023-03-07 17:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0007_alter_gender_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book",
            old_name="languages",
            new_name="language",
        ),
    ]