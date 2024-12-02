import http

import django.contrib.auth
import django.contrib.auth.tokens
import django.core.mail
import django.test
import django.urls
import django.utils.timezone


__all__ = ()


class SignupTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Назначение модели пользователя и URL для регистрации
        """
        super().setUpClass()
        cls.signup_url = django.urls.reverse("users:signup")
        cls.user = django.contrib.auth.get_user_model()

    def test_signup_sucsess(self):
        """
        Создание пользователя с правильными данными
        """
        response = self.client.post(
            self.signup_url,
            {
                self.user.username.field.name: "denis",
                self.user.email.field.name: "denis@mail.com",
                "password1": "hard02134",
                "password2": "hard02134",
            },
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertTrue(
            self.user.objects.filter(
                email="denis@mail.com",
            ).exists(),
        )

    def test_signup_sucsess_email_sended(self):
        """
        Проверка отправки письма
        """
        response = self.client.post(
            self.signup_url,
            {
                self.user.username.field.name: "denis",
                self.user.email.field.name: "denis@mail.com",
                "password1": "hard02134",
                "password2": "hard02134",
            },
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(len(django.core.mail.outbox), 1)

    def test_signup_unsucsess(self):
        """
        Невозможность создать пользователя с существующей почтой
        """
        self.user.objects.create(
            username="denis",
            email="denis@mail.com",
            password="hard02134",
        )

        self.client.post(
            self.signup_url,
            {
                self.user.username.field.name: "notdenis",
                self.user.email.field.name: "denis@mail.com",
                "password1": "hard02134",
                "password2": "hard02134",
            },
        )

        self.assertEqual(self.user.objects.count(), 1)

    def test_incorrect_username(self):
        """
        Невозможность создать пользователя с неверным ником
        """
        self.client.post(
            self.signup_url,
            {
                self.user.username.field.name: "",
                self.user.email.field.name: "denis@mail.com",
                "password1": "hard02134",
                "password2": "hard02134",
            },
        )
        self.assertEqual(self.user.objects.count(), 0)

    def test_incorrect_email(self):
        """
        Невозможность создать пользователя с неверной почтой
        """
        self.client.post(
            self.signup_url,
            {
                self.user.username.field.name: "denis",
                self.user.email.field.name: "denismail.com",
                "password1": "hard02134",
                "password2": "hard02134",
            },
        )
        self.assertEqual(self.user.objects.count(), 0)

    def test_incorrect_password(self):
        """
        Невозможность создать пользователя с разными паролями
        """
        self.client.post(
            self.signup_url,
            {
                self.user.username.field.name: "denis",
                self.user.email.field.name: "denis@mail.com",
                "password1": "hard02135",
                "password2": "hard02134",
            },
        )
        self.assertEqual(self.user.objects.count(), 0)


class UserActivationTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_model = django.contrib.auth.get_user_model()
        cls.user = cls.user_model.objects.create_user(
            username="denis",
            email="denis@example.com",
            password="maksim123",
            is_active=False,
            date_joined=django.utils.timezone.now()
            - django.utils.timezone.timedelta(hours=1),
        )

        cls.token_generator = (
            django.contrib.auth.tokens.PasswordResetTokenGenerator()
        )
        cls.token = cls.token_generator.make_token(cls.user)
        cls.activation_url = django.urls.reverse(
            "users:activate",
            args=[cls.user.username, cls.token],
        )

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
