import django.contrib.auth
import django.db.models


__all__ = ()


user_model = django.contrib.auth.get_user_model()


class NotificationsManager(django.db.models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)


class Notifications(django.db.models.Model):
    objects = NotificationsManager()

    user = django.db.models.ForeignKey(
        user_model,
        on_delete=django.db.models.CASCADE,
        null=True,
        related_name="user_notification",
    )
    name = django.db.models.CharField(
        max_length=20,
        verbose_name="название",
        help_text="название уведомления",
    )
    is_active = django.db.models.BooleanField(
        default=True,
        verbose_name="активно",
        help_text="активное уведомление",
    )
    is_active_day = django.db.models.BooleanField(
        default=True,
        verbose_name="активно",
        help_text="активное уведомление на день",
    )
    time = django.db.models.TimeField(
        verbose_name="время уведомления",
        help_text="время уведомления с точностью до минут",
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="время",
        help_text="время создания уведомления",
        null=True,
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name="время обновления",
        help_text="время последнего обновления",
        null=True,
    )

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"

    def __str__(self):
        return self.name
