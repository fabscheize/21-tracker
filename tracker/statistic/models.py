import django.db.models

import habits.models

__all__ = ()


class HabitLog(django.db.models.Model):
    habit = django.db.models.ForeignKey(
        habits.models.Habits,
        on_delete=django.db.models.CASCADE,
        related_name="logs",
    )
    date = django.db.models.DateField()
    progress = django.db.models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        unique_together = (
            "habit",
            "date",
        )

    def __str__(self):
        return f"{self.habit.name} - {self.date} ({self.progress}%)"


class HabitStats(django.db.models.Model):
    habit = django.db.models.OneToOneField(
        habits.models.Habits,
        on_delete=django.db.models.CASCADE,
        related_name="stats",
    )
    longest_streak = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="Самая длинная серия выполнения",
        help_text="Максимальное количество дней подряд, когда привычка была выполнена на 100%",
    )
    days_completed_current_month = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="Дни выполнения за месяц",
        help_text="Количество дней за текущий месяц, когда привычка была выполнена на 100%",
    )
    days_missed_current_month = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="Пропущенные дни за месяц",
        help_text="Количество дней за текущий месяц с прогрессом 0%",
    )
    last_reset = django.db.models.DateField(
        auto_now_add=True,
        verbose_name="Дата последнего сброса",
    )
