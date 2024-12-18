import datetime

import django.contrib.auth
import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views
import django.views.generic

import habits.forms
import habits.models
import statistic.models

__all__ = ()

user_model = django.contrib.auth.get_user_model()


class HabitsListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.base.TemplateResponseMixin,
    django.views.generic.View,
):
    template_name = "habits/list.html"

    def get(self, request, *args, **kwargs):
        all_habits = habits.models.Habits.objects.active().filter(
            user=request.user,
        )
        form = habits.forms.BaseHabitForm()
        return self.render_to_response({"habits": all_habits, "form": form})

    def post(self, request, *args, **kwargs):
        form = habits.forms.BaseHabitForm(request.POST)
        if form.is_valid():
            with django.db.transaction.atomic():
                habit = form.save(commit=False)
                habit.user = request.user
                habit.save()

                today = datetime.date.today()
                log, _ = statistic.models.HabitLog.objects.get_or_create(
                    habit=habit,
                    date=today,
                    defaults={"progress": 0},
                )

                log.save()

            return django.shortcuts.redirect(
                django.urls.reverse("habits:list"),
            )

        all_habits = habits.models.Habits.objects.active().filter(
            user=request.user,
        )
        return self.render_to_response({"habits": all_habits, "form": form})


class HabitCompleteView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def post(self, request, pk):
        habit = django.shortcuts.get_object_or_404(
            habits.models.Habits,
            id=pk,
            user=request.user,
        )

        with django.db.transaction.atomic():
            if habit.day_count < habit.count:
                habit.day_count += 1
                habit.save()

            today = datetime.date.today()
            log, _ = statistic.models.HabitLog.objects.get_or_create(
                habit=habit,
                date=today,
                defaults={"progress": 0},
            )
            if habit.day_count == habit.count:
                log.progress = 100
            else:
                log.progress = int((habit.day_count / habit.count) * 100)

            log.save()

            stats, _ = statistic.models.HabitStats.objects.get_or_create(
                habit=habit,
            )

            if log.progress == 100:
                stats.days_completed_current_month += 1

                previous_log = statistic.models.HabitLog.objects.filter(
                    habit=habit,
                    date=today - datetime.timedelta(days=1),
                    progress=100,
                ).exists()

                if previous_log:
                    stats.longest_streak += 1
                else:
                    stats.longest_streak = 1

            stats.save()

        return django.shortcuts.redirect(django.urls.reverse("habits:list"))


class HabitsSettingsView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.UpdateView,
):
    model = habits.models.Habits
    template_name = "habits/settings.html"
    form_class = habits.forms.BaseHabitForm
    success_url = django.urls.reverse_lazy("habits:list")

    def get_object(self, queryset=None):
        return self.model.objects.active().get(
            user=self.request.user,
            id=self.kwargs["pk"],
        )

    def form_valid(self, form):
        with django.db.transaction.atomic():
            habit = form.save(commit=False)
            habit.user = self.request.user
            count = form.cleaned_data.get(
                habits.models.Habits.count.field.name,
            )
            if count < habit.day_count:
                habit.day_count = count

            habit.save()

            today = datetime.date.today()
            log, _ = statistic.models.HabitLog.objects.get_or_create(
                habit=habit,
                date=today,
                defaults={"progress": 0},
            )
            if habit.day_count == habit.count:
                log.progress = 100
            else:
                log.progress = int((habit.day_count / habit.count) * 100)

            log.save()

        return super().form_valid(form)


class HabitsDeleteView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.DeleteView,
):
    model = habits.models.Habits
    success_url = django.urls.reverse_lazy("habits:list")

    def get_object(self, queryset=None):
        return self.model.objects.active().get(
            user=self.request.user,
            id=self.kwargs["pk"],
        )


class HabitsCountReloadView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def post(self, request, *args, **kwargs):
        habit = habits.models.Habits.objects.active().get(
            user=self.request.user,
            id=self.kwargs["pk"],
        )

        with django.db.transaction.atomic():
            habit.day_count = 0
            habit.save()

            today = datetime.date.today()
            log, _ = statistic.models.HabitLog.objects.get_or_create(
                habit=habit,
                date=today,
                defaults={"progress": 0},
            )
            log.save()

        return django.shortcuts.redirect(
            django.urls.reverse_lazy("habits:list"),
        )
