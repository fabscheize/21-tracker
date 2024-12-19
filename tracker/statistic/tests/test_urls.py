import django.test
import django.urls


__all__ = ()


class StatisticUrlsTest(django.test.TestCase):
    def test_progress_url(self):
        """
        Проверка работоспособности ссылки настроек
        """
        django.urls.reverse("statistic:progress")
