import django.urls

import habits.views


app_name = "habits"

urlpatterns = [
    django.urls.path(
        "",
        habits.views.HabitsListView.as_view(),
        name="list",
    ),
    django.urls.path(
        "create/",
        habits.views.HabitsCreateView.as_view(),
        name="create",
    ),
    django.urls.path(
        "<int:pk>/complete/",
        habits.views.HabitCompleteView.as_view(),
        name="complete",
    ),
    django.urls.path(
        "<int:pk>/",
        habits.views.HabitsSettingsView.as_view(),
        name="settings",
    ),
    django.urls.path(
        "<int:pk>/delete/",
        habits.views.HabitsDeleteView.as_view(),
        name="delete",
    ),
    django.urls.path(
        "<int:pk>/reload/",
        habits.views.HabitsCountReloadView.as_view(),
        name="reload",
    ),
]
