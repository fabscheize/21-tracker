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
