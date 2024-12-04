import django.contrib.auth.models
import django.db.models


__all__ = ()


class CustomUserManager(django.contrib.auth.models.UserManager):
    def active(self):
        return self.get_queryset().filter(is_active=True)


class User(django.contrib.auth.models.AbstractUser):
    objects = CustomUserManager()

    telegram_id = django.db.models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="телеграмм айди",
    )
    attempts_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="счетчик входов",
    )
    block_date = django.db.models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="время блокировки",
    )
