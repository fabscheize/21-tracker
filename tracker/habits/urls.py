import django.urls

import habits.views


app_name = "habits"

urlpatterns = [
    django.urls.path(
        "",
        habits.views.HabitsListView.as_view(),
        name="list",
    ),
]
