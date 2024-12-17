import django.apps


__all__ = ()


class StatisticConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "statistic"
    verbose_name = "Статистика"
