import django.contrib.auth
import django.contrib.messages
import django.urls
import django.utils.translation
import django.views.generic

import users.forms

_ = django.utils.translation.gettext
user_model = django.contrib.auth.get_user_model()

__all__ = ()


class SignupViewForm(django.views.generic.FormView):
    template_name = "users/signup.html"
    form_class = users.forms.SignupForm
    success_url = django.urls.reverse_lazy("homepage:main-data")

    def form_valid(self, form):
        if user_model.objects.filter(
            email=form.cleaned_data[user_model.email.field.name],
        ).exists():
            django.contrib.messages.error(
                self.request,
                _("Пользователь с такой почтой уже существует"),
            )
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.save()
        django.contrib.messages.success(
            self.request,
            _("Регистрация прошла успешно!"),
        )

        return super().form_valid(form)
