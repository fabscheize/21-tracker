import django.contrib.auth
import django.contrib.auth.forms


__all__ = ()

user_model = django.contrib.auth.get_user_model()


class SignupForm(django.contrib.auth.forms.UserCreationForm):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = user_model
        fields = [
            user_model.username.field.name,
            user_model.email.field.name,
        ]


class ChangeForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            if field.errors:
                field.field.widget.attrs["class"] += " is-invalid"

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = [
            user_model.first_name.field.name,
            user_model.last_name.field.name,
            user_model.email.field.name,
        ]
        labels = {
            user_model.first_name.field.name: "Имя",
            user_model.last_name.field.name: "Фамилия",
            user_model.email.field.name: "Почта",
        }
