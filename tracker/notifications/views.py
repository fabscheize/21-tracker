import datetime

import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.messages
import django.db
import django.db.models
import django.forms
import django.shortcuts
import django.urls
import django.utils.timezone
import django.utils.translation
import django.views
import django.views.generic
import pytz

import notifications.forms
import notifications.models

__all__ = ()

_ = django.utils.translation.gettext

user_model = django.contrib.auth.get_user_model()


class NotificationListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.FormView,
):
    template_name = "notifications/settings.html"
    form_class = notifications.forms.NotificationsForm
    success_url = django.urls.reverse_lazy("notifications:settings")

    def get_object(self):
        return notifications.models.Notifications.objects.filter(
            user=self.request.user,
        ).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notification"] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_object()
        if instance:
            kwargs["instance"] = instance

        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        start_time = form.cleaned_data.get(
            notifications.models.Notifications.start_time.field.name,
        )
        end_time = form.cleaned_data.get(
            notifications.models.Notifications.end_time.field.name,
        )
        if end_time > start_time:
            today = datetime.date.today()
            start_datetime = datetime.datetime.combine(today, start_time)
            end_datetime = datetime.datetime.combine(today, end_time)

            user_timezone = pytz.timezone(form.instance.user.timezone)
            aware_start_time = user_timezone.localize(start_datetime)
            aware_end_time = user_timezone.localize(end_datetime)

            server_tz = django.utils.timezone.get_current_timezone()
            server_start_time = aware_start_time.astimezone(server_tz)
            server_end_time = aware_end_time.astimezone(server_tz)

            form.instance.start_time = start_time.strftime("%H:%M")
            form.instance.end_time = end_time.strftime("%H:%M")
            form.instance.start_server_time = server_start_time.strftime(
                "%H:%M",
            )
            form.instance.end_server_time = server_end_time.strftime("%H:%M")

            django.contrib.messages.success(
                self.request,
                _("Успешно сохранено"),
            )

            form.save()
            return super().form_valid(form)

        django.contrib.messages.error(
            self.request,
            _("Интервал времени некорректный"),
        )
        return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class NotificationActiveControlView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):

    def post(self, request, *args, **kwargs):
        notification = django.shortcuts.get_object_or_404(
            notifications.models.Notifications,
            user=request.user,
        )

        notification.is_active = not notification.is_active
        notification.save()

        notification.save()
        return django.shortcuts.redirect(
            django.urls.reverse_lazy("notifications:settings"),
        )
