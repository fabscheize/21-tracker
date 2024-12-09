import django.contrib.auth
import django.contrib.auth.models
import django.test


__all__ = ()

user_model = django.contrib.auth.get_user_model()


class CustomBackendTest(django.test.TestCase):
    def setUp(self):
        self.user = user_model.objects.create(
            username="test",
            password="test",
        )
        self.factory = django.test.RequestFactory()

    def test_authenticated_user(self):
        """
        Проверка с авторизованным пользователем
        """
        request = self.factory.get("/")
        request.user = self.user

        updated_user = user_model.objects.get(pk=self.user.pk)
        self.assertEqual(request.user, updated_user)

    def test_anonymous_user(self):
        """
        Проверка с анонимным пользователем
        """
        request = self.factory.get("/")
        request.user = django.contrib.auth.models.AnonymousUser()
        self.assertTrue(
            isinstance(request.user, django.contrib.auth.models.AnonymousUser),
        )
