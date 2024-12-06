import django.views.generic

__all__ = ()


class HabitsListView(django.views.generic.TemplateView):
    template_name = "habits/list.html"
