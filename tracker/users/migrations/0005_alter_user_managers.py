# Generated by Django 4.2.16 on 2024-12-07 12:46

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_merge_20241204_2052"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", users.models.CustomUserManager()),
            ],
        ),
    ]
