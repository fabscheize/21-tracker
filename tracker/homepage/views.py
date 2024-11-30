import django.views.generic


__all__ = ()


class HomepageView(django.views.generic.TemplateView):
    template_name = "homepage/main_data.html"
