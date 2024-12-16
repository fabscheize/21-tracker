import os

import celery
import celery.schedules

__all__ = ()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker.settings")

app = celery.Celery("tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
