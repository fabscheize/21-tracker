import django.contrib.admin
import django.urls


__all__ = ()

path = django.urls.path
include = django.urls.include

urlpatterns = [
    path("", include("homepage.urls", namespace="homepage")),
    path("admin/", django.contrib.admin.site.urls),
]


if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )
