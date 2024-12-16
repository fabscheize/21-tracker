import django.contrib.auth
import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views
import django.views.generic

import notifications.forms
import notifications.models

__all__ = ()

user_model = django.contrib.auth.get_user_model()


class NotificationListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.base.TemplateResponseMixin,
    django.views.generic.View,
):
    template_name = "notifications/list.html"

    def get(self, request, *args, **kwargs):
        all_notifications = (
            notifications.models.Notifications.objects.active().filter(
                user=request.user,
            )
        )
        form = notifications.forms.NotificationsForm()
        return self.render_to_response(
            {"notifications": all_notifications, "form": form},
        )

    def post(self, request, *args, **kwargs):
        form = notifications.forms.NotificationsForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return django.shortcuts.redirect(
                django.urls.reverse("notifications:settings"),
            )

        all_notifications = (
            notifications.models.Notifications.objects.active().filter(
                user=request.user,
            )
        )
        return self.render_to_response(
            {"notifications": all_notifications, "form": form},
        )


class NotificationDeleteView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.DeleteView,
):
    model = notifications.models.Notifications
    success_url = django.urls.reverse_lazy("notifications:settings")

    def get_object(self, queryset=None):
        return self.model.objects.active().get(
            user=self.request.user,
            id=self.kwargs["pk"],
        )
