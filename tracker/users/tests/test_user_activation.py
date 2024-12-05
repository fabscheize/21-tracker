import django.conf
import django.contrib.auth
import django.contrib.auth.tokens
import django.core.mail
import django.test
import django.urls
import django.utils.timezone
import freezegun


__all__ = ()


class UserActivationTest(django.test.TestCase):
    @classmethod
    @freezegun.freeze_time("2024-12-03")
    def setUpTestData(cls):
        cls.user_model = django.contrib.auth.get_user_model()
        cls.user = cls.user_model.objects.create_user(
            username="denis",
            email="denis@example.com",
            password="maksim123",
            is_active=False,
            date_joined=django.utils.timezone.now(),
        )

        cls.token_generator = (
            django.contrib.auth.tokens.PasswordResetTokenGenerator()
        )
        cls.token = cls.token_generator.make_token(cls.user)
        cls.activation_url = django.urls.reverse(
            "users:activate",
            args=[cls.user.username, cls.token],
        )

    @freezegun.freeze_time("2024-12-03")
    def test_user_activated(self):
        """
        Проверка активации пользователя после перехода по ссылке
        """
        self.client.get(self.activation_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_user_activate_invalid_token(self):
        """
        Проверка активации с неверным токеном
        """
        invalid_token_url = django.urls.reverse(
            "users:activate",
            args=[self.user.username, "неверный токен"],
        )

        self.client.get(invalid_token_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    @freezegun.freeze_time("2024-12-03")
    def test_user_activation_expired_link(self):
        """
        Проверка с истекшей ссылкой
        """
        self.user.date_joined = (
            django.utils.timezone.now()
            - django.utils.timezone.timedelta(days=2)
        )

        self.user.save()
        self.client.get(self.activation_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
