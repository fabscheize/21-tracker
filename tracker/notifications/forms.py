import django.forms
import django.utils.translation

import notifications.models


__all__ = ()


class NotificationsForm(django.forms.ModelForm):
    time = django.forms.TimeField(
        widget=django.forms.TimeInput(
            attrs={"type": "time", "class": "form-control"},
        ),
        label=django.utils.translation.gettext_lazy("Время отправки"),
        help_text=django.utils.translation.gettext_lazy(
            "Когда мне нужно отправить уведомление",
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
            notifications.models.Notifications.time.field.name,
        ]
        labels = {
            notifications.models.Notifications.name.field.name: (
                django.utils.translation.gettext_lazy("Текст уведомления")
            ),
            notifications.models.Notifications.time.field.name: (
                django.utils.translation.gettext_lazy("Время отправки")
            ),
        }
        help_texts = {
            notifications.models.Notifications.name.field.name: (
                django.utils.translation.gettext_lazy("Обязательное поле")
            ),
            notifications.models.Notifications.time.field.name: (
                django.utils.translation.gettext_lazy(
                    "Когда мне нужно отправить уведомление",
                )
            ),
        }
