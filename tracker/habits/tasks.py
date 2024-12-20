import celery
import django.contrib.auth
import django.utils.timezone
import pytz

import habits.models


user_model = django.contrib.auth.get_user_model()

__all__ = ()


@celery.shared_task
def perodic_reload_task():
    working_tz = get_timezones()
    reset_habit_counts(working_tz)


def get_timezones():
    working_tz = []
    current_time = django.utils.timezone.now()

    for tz_name in pytz.all_timezones:
        tz = pytz.timezone(tz_name)
        current_time_in_tz = current_time.astimezone(tz)
        count_time = current_time_in_tz - django.utils.timezone.timedelta(
            hours=1,
        )

        if current_time_in_tz.day != count_time.day:
            working_tz.append(tz)

    return working_tz


def reset_habit_counts(timezones):
    for tz in timezones:
        habit_list = habits.models.Habits.objects.filter(user__timezone=tz)
        for habit in habit_list:
            habit.day_count = 0
            habit.save()
