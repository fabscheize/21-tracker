import django.conf
import django.contrib.auth
import django.contrib.auth.tokens
import django.core.mail
import django.test
import django.urls
import django.utils.timezone
import freezegun


__all__ = ()


class LoginBackendTest(django.test.TestCase):
    @classmethod
    @freezegun.freeze_time("2024-12-03")
    def setUpTestData(cls):
        cls.login_url = django.urls.reverse("users:login")
        cls.user_model = django.contrib.auth.get_user_model()
        cls.user_password = "maksim123"
        cls.user = cls.user_model.objects.create_user(
            username="denis",
            email="denis@example.com",
            password=cls.user_password,
            is_active=True,
            date_joined=django.utils.timezone.now(),
        )
        cls.token_generator = (
            django.contrib.auth.tokens.PasswordResetTokenGenerator()
        )
        cls.token = cls.token_generator.make_token(cls.user)
        cls.activation_url = django.urls.reverse(
            "users:re-activate",
            args=[cls.user.username, cls.token],
        )

    def test_user_by_email(self):
        login_success = self.client.login(
            username=self.user.email,
            password=self.user_password,
        )
        self.assertTrue(login_success)

    @django.test.override_settings(MAX_AUTH_ATTEMPTS=3)
    def test_user_block(self):
        """
        Проверка на блокировку при превышении попыток
        """
        for _ in range(2):
            # используем не login() т.к при блокировке создается url активации
            self.client.post(
                self.login_url,
                {
                    self.user_model.username.field.name: self.user.username,
                    "password": "234234324234",
                },
            )
            self.user.refresh_from_db()
            self.assertEqual(self.user.is_active, True)

        self.client.post(
            self.login_url,
            {
                self.user_model.username.field.name: self.user.username,
                self.user_model.password.field.name: "maks12345",
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_active, False)

    @django.test.override_settings(MAX_AUTH_ATTEMPTS=1)
    def test_mail_send(self):
        """
        Проверка на отправку письма
        """
        self.client.post(
            self.login_url,
            {
                self.user_model.username.field.name: self.user.username,
                self.user_model.password.field.name: "maks12345",
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_active, False)
        self.assertEqual(len(django.core.mail.outbox), 1)

    @django.test.override_settings(MAX_AUTH_ATTEMPTS=1)
    @freezegun.freeze_time("2024-12-05")
    def test_user_activated(self):
        """
        Проверка активации пользователя после перехода по ссылке
        """
        self.client.post(
            self.login_url,
            {
                self.user_model.username.field.name: self.user.username,
                self.user_model.password.field.name: "maks12345",
            },
        )

        self.client.get(self.activation_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    @django.test.override_settings(MAX_AUTH_ATTEMPTS=1)
    @freezegun.freeze_time("2024-12-05")
    def test_user_activate_invalid_token(self):
        """
        Проверка активации с неверным токеном
        """
        invalid_token_url = django.urls.reverse(
            "users:activate",
            args=[self.user.username, "неверный токен"],
        )
        self.client.post(
            self.login_url,
            {
                self.user_model.username.field.name: self.user.username,
                self.user_model.password.field.name: "maks12345",
            },
        )
        self.client.get(invalid_token_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    @django.test.override_settings(MAX_AUTH_ATTEMPTS=1)
    @freezegun.freeze_time("2024-12-05")
    def test_user_activation_expired_link(self):
        """
        Проверка с истекшей ссылкой
        """
        self.client.post(
            self.login_url,
            {
                self.user_model.username.field.name: self.user.username,
                self.user_model.password.field.name: "maks12345",
            },
        )
        self.user.refresh_from_db()
        self.user.block_date = (
            django.utils.timezone.now()
            - django.utils.timezone.timedelta(days=8)
        )
        self.user.save()
        self.client.get(self.activation_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
