import django.contrib.auth
import django.db.models
import django.utils.timezone


__all__ = ()


user_model = django.contrib.auth.get_user_model()


class NotificationsManager(django.db.models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)


class Notifications(django.db.models.Model):
    class NotificationsChoices(django.db.models.TextChoices):
        FIVE_MIN = "5min", "5 минут"
        FITH_MIN = "15min", "15 минут"
        THIR_MIN = "30min", "30 минут"
        ONE_HOUR = "1hour", "1 час"
        THREE_HOURS = "3hours", "3 часа"

    objects = NotificationsManager()

    user = django.db.models.OneToOneField(
        user_model,
        on_delete=django.db.models.CASCADE,
        null=False,
        blank=False,
        related_name="user_notification",
    )
    name = django.db.models.CharField(
        max_length=20,
        verbose_name="название",
        help_text="название уведомления",
        null=False,
        blank=False,
    )
    is_active = django.db.models.BooleanField(
        default=True,
        verbose_name="активно",
        help_text="активное уведомление",
    )
    periodic_time = django.db.models.CharField(
        max_length=10,
        verbose_name="период отправки уведомления",
        help_text="период отправки уведомления с точностью до минут",
        choices=NotificationsChoices.choices,
        null=False,
        blank=False,
    )
    start_time = django.db.models.TimeField(
        verbose_name="начало отправки уведомлений",
        help_text="время начала отправки уведомлений",
        null=False,
        blank=False,
    )
    end_time = django.db.models.TimeField(
        verbose_name="конец отправки уведомлений",
        help_text="время конца отправки уведомлений",
        null=False,
        blank=False,
    )
    start_server_time = django.db.models.TimeField(
        verbose_name="начало отправки уведомлений",
        help_text="серверное время начала отправки уведомлений",
        null=True,
    )
    end_server_time = django.db.models.TimeField(
        verbose_name="конец отправки уведомлений",
        help_text="серверное время конца отправки уведомлений",
        null=True,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="время",
        help_text="время создания уведомления",
        null=False,
        blank=False,
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name="время обновления",
        help_text="время последнего обновления",
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"

    def __str__(self):
        return self.name
