import django.contrib.auth.models
import django.db.models


__all__ = ()


class User(django.contrib.auth.models.AbstractUser):
    telegram_id = django.db.models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="telegram_id",
    )
