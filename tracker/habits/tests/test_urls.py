import django.test
import django.urls


__all__ = ()


class HabitsUrlsTest(django.test.TestCase):
    def test_list_url(self):
        """
        Проверка работаспособности ссылки списка
        """
        django.urls.reverse("habits:list")

    def test_complete_url(self):
        """
        Проверка работаспособности ссылки выполнения
        """
        django.urls.reverse("habits:complete", args=[1])

    def test_settings_url(self):
        """
        Проверка работаспособности ссылки настроек
        """
        django.urls.reverse("habits:settings", args=[1])

    def test_delete_url(self):
        """
        Проверка работаспособности ссылки удаления
        """
        django.urls.reverse("habits:delete", args=[1])

    def test_reload_url(self):
        """
        Проверка работаспособности ссылки перезагрузки привычек
        """
        django.urls.reverse("habits:reload", args=[1])
