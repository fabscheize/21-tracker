import http

import django.contrib.auth
import django.test
import django.urls

__all__ = []


user_model = django.contrib.auth.get_user_model()


class StatisticViewsTest(django.test.TestCase):
    def setUp(self):
        """
        Создание тестового пользователя
        """
        self.user = user_model.objects.create_user(
            username="testuser", password="password",
        )

    def test_progress_view(self):
        """
        Проверка страницы прогресса
        """
        self.client.login(username="testuser", password="password")

        response = self.client.get(
            django.urls.reverse("statistic:progress"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
