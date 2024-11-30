import http

import django.test
import django.urls

__all__ = ()


class HomepageTest(django.test.TestCase):
    def test_homepage_status(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:main-data"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
