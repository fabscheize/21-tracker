import django.urls

import statistic.views


app_name = "statistic"

urlpatterns = [
    django.urls.path(
        "",
        statistic.views.ProgressView.as_view(),
        name="progress",
    ),
]
