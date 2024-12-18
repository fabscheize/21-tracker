import celery
import django.conf
import django.contrib.auth
import django.core.mail
import django.utils.timezone
import django.utils.translation

import notifications.models as not_model

_ = django.utils.translation.gettext
user_model = django.contrib.auth.get_user_model()

__all__ = ()


def perodic_notifications_base(period):
    notifications = not_model.Notifications.objects.active().filter(
        periodic_time=period,
    )
    if notifications:
        filtered_notifications = filter_notifications(notifications)
        sending_mail(filtered_notifications)


@celery.shared_task
def perodic_notifications_task_five():
    perodic_notifications_base("5min")


@celery.shared_task
def perodic_notifications_task_fifteen():
    perodic_notifications_base("15min")


@celery.shared_task
def perodic_notifications_task_thirty():
    perodic_notifications_base("30min")


@celery.shared_task
def perodic_notifications_task_hour():
    perodic_notifications_base("1hour")


@celery.shared_task
def perodic_notifications_task_hours():
    perodic_notifications_base("3hours")


def filter_notifications(notifications):
    now = django.utils.timezone.now().replace(second=0, microsecond=0)
    now_time = now.time()
    filtered_notifications = []

    for nots in notifications:
        start_time = nots.start_server_time
        end_time = nots.end_server_time

        if start_time <= end_time:
            if start_time <= now_time <= end_time:
                filtered_notifications.append(nots)
        else:
            if now_time >= start_time or now_time <= end_time:
                filtered_notifications.append(nots)

    return filtered_notifications


def sending_mail(filtered_notifications):
    for nots in filtered_notifications:
        django.core.mail.send_mail(
            subject=("Напоминание"),
            message=nots.name,
            from_email=django.conf.settings.DJANGO_MAIL,
            recipient_list=[nots.user.email],
            fail_silently=False,
        )
