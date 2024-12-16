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
        "<int:pk>/delete/",
        notifications.views.NotificationDeleteView.as_view(),
        name="delete",
    ),
]
