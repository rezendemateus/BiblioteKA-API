# Generated by Django 4.1.7 on 2023-03-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0006_alter_gender_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gender",
            name="name",
            field=models.CharField(max_length=150),
        ),
    ]