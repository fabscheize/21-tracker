import django.contrib.admin
import django.contrib.auth
import django.contrib.auth.urls
import django.urls


__all__ = ()

path = django.urls.path
include = django.urls.include

urlpatterns = [
    path("", include("homepage.urls", namespace="homepage")),
    path("admin/", django.contrib.admin.site.urls),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include(django.contrib.auth.urls)),
    path("habits/", include("habits.urls", namespace="habits")),
    path("statistic/", include("statistic.urls", namespace="statistic")),
    path(
        "settings/",
        include("notifications.urls", namespace="notifications"),
    ),
]


if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )
