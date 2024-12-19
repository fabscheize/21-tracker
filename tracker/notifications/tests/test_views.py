import http

import django.contrib.auth
import django.test
import django.urls


__all__ = ()


class NotificationsViewsTest(django.test.TestCase):
    def test_settings_view(self):
        """
        Проверка страницы настроек уведомлений
        """
        response = self.client.get(
            django.urls.reverse("notifications:settings"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)

    def test_control_view(self):
        """
        Проверка страницы контроля уведомлений
        """
        response = self.client.get(
            django.urls.reverse("notifications:control"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
