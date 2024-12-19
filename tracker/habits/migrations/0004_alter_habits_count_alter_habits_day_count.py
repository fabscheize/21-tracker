# Generated by Django 4.2.16 on 2024-12-19 12:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0003_alter_habits_count_alter_habits_day_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habits",
            name="count",
            field=models.PositiveSmallIntegerField(
                default=1,
                help_text="сколько раз нужно выполнить привычку за день",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="число выполнений",
            ),
        ),
        migrations.AlterField(
            model_name="habits",
            name="day_count",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="сколько раз была выполнена привычка за день",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="число выполнений в день",
            ),
        ),
    ]
