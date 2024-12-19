import django.forms
import django.utils.translation

import habits.models


__all__ = ()


class BaseHabitForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            if field.errors:
                field.field.widget.attrs["class"] += " is-invalid"

    class Meta:
        model = habits.models.Habits
        fields = [
            habits.models.Habits.name.field.name,
            habits.models.Habits.count.field.name,
        ]
        labels = {
            habits.models.Habits.name.field.name: (
                django.utils.translation.gettext_lazy("Имя привычки")
            ),
            habits.models.Habits.count.field.name: (
                django.utils.translation.gettext_lazy("Цель")
            ),
        }
        help_texts = {
            habits.models.Habits.name.field.name: (
                django.utils.translation.gettext_lazy("Обязательное поле")
            ),
            habits.models.Habits.count.field.name: (
                django.utils.translation.gettext_lazy(
                    "Сколько раз выполнять привычку за день (от 1 до 100)",
                )
            ),
        }
        error_messages = {
            habits.models.Habits.count.field.name: {
                "min_value": django.utils.translation.gettext_lazy(
                    "Значение должно быть не меньше 1.",
                ),
                "max_value": django.utils.translation.gettext_lazy(
                    "Значение должно быть не больше 100.",
                ),
            },
        }
