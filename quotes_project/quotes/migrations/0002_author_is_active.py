# Generated by Django 5.0.3 on 2024-03-25 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
