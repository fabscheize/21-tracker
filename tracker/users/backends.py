import django.conf
import django.contrib.auth
import django.contrib.auth.backends
import django.contrib.auth.tokens
import django.core
import django.core.mail
import django.urls
import django.utils
import django.utils.timezone
import django.utils.translation


__all__ = ()

user_model = django.contrib.auth.get_user_model()
activation_token = django.contrib.auth.tokens.PasswordResetTokenGenerator()
_ = django.utils.translation.gettext


class CustomBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = (
                user_model.objects.active().get(email=username)
                if "@" in username
                else user_model.objects.active().get(username=username)
            )
        except user_model.DoesNotExist:
            user = None

        if user:
            if user.check_password(password):
                user.attempts_count = 0
                user.save()
                return user

            user.attempts_count += 1
            user.save()
            if user.attempts_count >= django.conf.settings.MAX_AUTH_ATTEMPTS:
                user.block_date = django.utils.timezone.now()
                user.is_active = False
                user.save()

                activation_url = request.build_absolute_uri(
                    django.urls.reverse(
                        "users:re-activate",
                        args=[
                            username,
                            activation_token.make_token(user),
                        ],
                    ),
                )

                django.core.mail.send_mail(
                    subject=_("Разморозка аккаунта"),
                    message=_("Ссылка для разморозки: ") + activation_url,
                    from_email=django.conf.settings.DJANGO_MAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )

                return user

        return None

    def get_user(self, user_id):
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
