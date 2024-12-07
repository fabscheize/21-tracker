import django.contrib.auth
import django.db.models


__all__ = ()

user_model = django.contrib.auth.get_user_model()


class Habits(django.db.models.Model):
    user = django.db.models.ForeignKey(
        user_model,
        on_delete=django.db.models.CASCADE,
        null=True,
        related_name="user_habit",
    )
    name = django.db.models.CharField(
        max_length=20,
        verbose_name="название",
        help_text="название привычки",
    )
    is_active = django.db.models.BooleanField(
        default=True,
        verbose_name="активно",
        help_text="активная привычка",
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="время",
        help_text="время создания привычки",
        null=True,
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name="время обновления",
        help_text="время последнего обновления",
        null=True,
    )
    count = django.db.models.SmallIntegerField(
        default=1,
        verbose_name="число выполнений",
        help_text="сколько раз нужно выполнить привычку за день",
    )
    day_count = django.db.models.SmallIntegerField(
        default=0,
        verbose_name="число выполнений в день",
        help_text="сколько раз была выполнена привычка за день",
    )

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return self.name
