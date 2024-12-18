import django.urls

import notifications.views


app_name = "notifications"

urlpatterns = [
    django.urls.path(
        "",
        notifications.views.NotificationListView.as_view(),
        name="settings",
    ),
    django.urls.path(
        "control/",
        notifications.views.NotificationActiveControlView.as_view(),
        name="control",
    ),
]
