import django.contrib.auth
import django.db
import django.db.models
import django.test

import habits.models

__all__ = ()

user_model = django.contrib.auth.get_user_model()


class HaditsModelsTest(django.test.TestCase):
    def setUp(self):
        self.user = user_model.objects.create(username="test", password="test")
        self.habit = habits.models.Habits.objects.create(
            name="habit",
            day_count=4,
            count=5,
            user=self.user,
        )

    def test_item_creation(self):
        """
        Проверка создания объекта (наличие его основных полей)
        """
        self.assertEqual(self.habit.name, "habit")
        self.assertEqual(self.habit.day_count, 4)
        self.assertEqual(self.habit.count, 5)
        self.assertEqual(self.habit.user, self.user)

    def test_progress_method(self):
        """
        Проверка получения прогресса
        """
        data = int((self.habit.day_count / self.habit.count) * 100)
        self.assertEqual(self.habit.progress(), data)
