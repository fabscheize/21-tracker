import django.forms
import django.utils.translation

import notifications.models


__all__ = ()


class NotificationsForm(django.forms.ModelForm):
    start_time = django.forms.TimeField(
        widget=django.forms.TimeInput(
            attrs={"type": "time"},
        ),
        label=django.utils.translation.gettext_lazy(
            "Время начала отправки уведомлений",
        ),
        help_text=django.utils.translation.gettext_lazy(
            "В какое время начинать отправлять вам уведомления",
        ),
    )
    end_time = django.forms.TimeField(
        widget=django.forms.TimeInput(
            attrs={"type": "time"},
        ),
        label=django.utils.translation.gettext_lazy(
            "Время конца отправки уведомлений",
        ),
        help_text=django.utils.translation.gettext_lazy(
            "В какое время перестать отправлять вам уведомления",
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            if field.errors:
                field.field.widget.attrs["class"] += " is-invalid"

    class Meta:
        model = notifications.models.Notifications
        fields = [
            notifications.models.Notifications.name.field.name,
            notifications.models.Notifications.periodic_time.field.name,
            notifications.models.Notifications.start_time.field.name,
            notifications.models.Notifications.end_time.field.name,
        ]
        labels = {
            notifications.models.Notifications.name.field.name: (
                django.utils.translation.gettext_lazy("Текст уведомления")
            ),
        }
        help_texts = {
            notifications.models.Notifications.name.field.name: (
                django.utils.translation.gettext_lazy("Обязательное поле")
            ),
        }
