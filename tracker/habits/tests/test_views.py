import http

import django.contrib.auth
import django.test
import django.urls

import habits.models

__all__ = ()


user_model = django.contrib.auth.get_user_model()


class HabitsViewsTest(django.test.TestCase):
    def setUp(self):
        self.user = user_model.objects.create(username="test")
        self.user.set_password("test")
        self.user.save()
        self.client.login(username="test", password="test")
        self.habit = habits.models.Habits.objects.create(
            name="habit",
            day_count=3,
            count=5,
            user=self.user,
        )

    def test_list_view(self):
        """
        Проверка страницы списка привычек
        """
        response = self.client.get(django.urls.reverse("habits:list"))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.habit.name)

    def test_create_view(self):
        """
        Проверка создания привычки
        """
        data = {
            habits.models.Habits.name.field.name: "habit1",
            habits.models.Habits.count.field.name: 10,
        }
        response = self.client.post(django.urls.reverse("habits:create"), data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertTrue(
            habits.models.Habits.objects.filter(
                name=data[habits.models.Habits.name.field.name],
            ).exists(),
        )

    def test_settings_view(self):
        """
        Проверка настройки привычки
        """
        url = django.urls.reverse("habits:settings", args=[self.habit.id])
        data = {
            habits.models.Habits.name.field.name: "1habit1",
            habits.models.Habits.count.field.name: 11,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, "1habit1")
        self.assertEqual(self.habit.count, 11)

    def test_settings_count_refresh_view(self):
        """
        Проверка настройки привычки если общий счетчик стал меньше дневного
        """
        url = django.urls.reverse("habits:settings", args=[self.habit.id])
        self.habit.day_count = 14
        self.habit.save()
        data = {
            habits.models.Habits.name.field.name: "1habit1",
            habits.models.Habits.count.field.name: 11,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, "1habit1")
        self.assertEqual(self.habit.count, 11)
        self.assertEqual(self.habit.day_count, 11)

    def test_complete_view(self):
        """
        Проверка увеличения дневного счетчика привычки по кнопке
        """
        url = django.urls.reverse("habits:complete", args=[self.habit.id])
        self.assertEqual(self.habit.day_count, 3)
        response = self.client.post(url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.day_count, 4)

    def test_complete_try_view(self):
        """
        Проверка что после предела(счетчика) дневной счетчик не увеличивается
        """
        self.habit.count = 3
        self.habit.save()
        url = django.urls.reverse("habits:complete", args=[self.habit.id])
        self.assertEqual(self.habit.day_count, 3)
        response = self.client.post(url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.day_count, 3)

    def test_delete_view(self):
        """
        Проверка удаления привычки
        """
        url = django.urls.reverse("habits:delete", args=[self.habit.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertFalse(
            habits.models.Habits.objects.filter(id=self.habit.id).exists(),
        )

    def test_reload_view(self):
        """
        Проверка обнуления дневного счетчика привычки
        """
        url = django.urls.reverse("habits:reload", args=[self.habit.id])
        self.assertEqual(self.habit.day_count, 3)
        response = self.client.post(url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.day_count, 0)
