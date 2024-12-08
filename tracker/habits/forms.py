import django.forms

import habits.models


__all__ = ()


class BaseHabitForm(django.forms.ModelForm):
    class Meta:
        model = habits.models.Habits
        fields = [
            habits.models.Habits.name.field.name,
            habits.models.Habits.count.field.name,
        ]
