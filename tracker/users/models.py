import django.conf
import django.contrib.auth.models
import django.db.models
import pytz


__all__ = ()

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]


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
    timezone = django.db.models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        verbose_name="часовой пояс пользователя",
        default=django.conf.settings.CELERY_TIMEZONE,
    )
