import django.contrib.auth
import django.test

import habits.forms
import habits.models

__all__ = ()


user_model = django.contrib.auth.get_user_model()


class BaseHabitFormTest(django.test.TestCase):
    def setUp(self):
        self.user = user_model.objects.create(username="test", password="test")
        self.habit_data = {
            habits.models.Habits.name.field.name: "habit",
            habits.models.Habits.count.field.name: 3,
        }

    def test_valid_data(self):
        """
        Проверка валидности формы с верными данными
        """
        form = habits.forms.BaseHabitForm(data=self.habit_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """
        Проверка валидности формы с неверными данными
        """
        invalid_data = {
            habits.models.Habits.name.field.name: "",
            habits.models.Habits.count.field.name: 3,
        }
        form = habits.forms.BaseHabitForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn(habits.models.Habits.name.field.name, form.errors)

    def test_form_save(self):
        """
        Проверка сохранения объекта после отправки формы
        """
        form = habits.forms.BaseHabitForm(data=self.habit_data)
        self.assertTrue(form.is_valid())
        habit = form.save(commit=False)
        habit.user = self.user
        habit.save()
        done_habit = habits.models.Habits.objects.get(id=habit.id)
        self.assertEqual(
            done_habit.name,
            self.habit_data[habits.models.Habits.name.field.name],
        )
        self.assertEqual(
            done_habit.count,
            self.habit_data[habits.models.Habits.count.field.name],
        )
