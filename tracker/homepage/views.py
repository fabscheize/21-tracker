import django.shortcuts
import django.urls
import django.views.generic


__all__ = ()


class HomepageView(django.views.generic.TemplateView):
    template_name = "homepage/welcome.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return django.shortcuts.redirect(
                django.urls.reverse("habits:list"),
            )

        return super().dispatch(request, *args, **kwargs)
