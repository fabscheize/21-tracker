import django.apps


__all__ = ()


class NotificationsConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
    verbose_name = "Уведомления"
