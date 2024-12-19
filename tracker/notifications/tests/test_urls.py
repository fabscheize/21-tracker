import django.test
import django.urls


__all__ = ()


class NotificationsUrlsTest(django.test.TestCase):
    def test_settings_url(self):
        """
        Проверка работоспособности ссылки настроек
        """
        django.urls.reverse("notifications:settings")

    def test_control_url(self):
        """
        Проверка работоспособности контроля уведомлений
        """
        django.urls.reverse("notifications:control")
