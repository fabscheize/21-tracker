import django.apps


__all__ = ()


class HabitsConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "habits"
    verbose_name = "Привычки"
