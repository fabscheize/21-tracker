import django.conf
import django.contrib.auth
import django.contrib.auth.tokens
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.utils.safestring
import django.utils.timezone
import django.utils.translation
import django.views.generic

import users.forms

_ = django.utils.translation.gettext
user_model = django.contrib.auth.get_user_model()
activation_token = django.contrib.auth.tokens.PasswordResetTokenGenerator()

__all__ = ()


class SignupViewForm(django.views.generic.FormView):
    template_name = "users/signup.html"
    form_class = users.forms.SignupForm
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        if user_model.objects.filter(
            email=form.cleaned_data[user_model.email.field.name],
        ).exists():
            django.contrib.messages.error(
                self.request,
                _("Пользователь с такой почтой уже существует"),
            )
            return super().form_invalid(form)

        user = form.save(commit=False)
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        activation_url = self.request.build_absolute_uri(
            django.urls.reverse(
                "users:activate",
                args=[user.username, activation_token.make_token(user)],
            ),
        )

        django.core.mail.send_mail(
            subject=_("Подтверждение регистрации"),
            message=_("Для активации перейдите по ссылке: ") + activation_url,
            from_email=django.conf.settings.DJANGO_MAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

        django.contrib.messages.success(
            self.request,
            django.utils.safestring.mark_safe(
                "<b>"
                + _("Регистрация прошла успешно!")
                + "</b><br>"
                + _(
                    "Чтобы активировать свой аккаунт перейдите по ссылке "
                    "в отправленном нами письме",
                ),
            ),
        )

        return super().form_valid(form)


class ActiveView(django.views.generic.base.View):
    def get(self, request, username, token):
        user = user_model.objects.get(username=username)
        time_elapsed = django.utils.timezone.now() - user.date_joined
        if not activation_token.check_token(user, token):
            return django.shortcuts.HttpResponse(_("Неверный токен."))

        elif time_elapsed > django.utils.timezone.timedelta(hours=7):
            return django.shortcuts.HttpResponse(
                _("Ссылка активации истекла."),
            )

        user.is_active = True
        user.save()
        return django.shortcuts.redirect("users:login")


class ReActiveView(django.views.generic.base.View):
    def get(self, request, username, token):
        user = user_model.objects.get(username=username)
        time_elapsed = django.utils.timezone.now() - user.block_date
        if not activation_token.check_token(user, token):
            return django.shortcuts.HttpResponse(_("Неверный токен."))

        elif time_elapsed > django.utils.timezone.timedelta(days=7):
            return django.shortcuts.HttpResponse(
                _("Ссылка активации истекла."),
            )

        user.is_active = True
        user.attempts_count = 0
        user.save()
        return django.shortcuts.redirect("users:login")
