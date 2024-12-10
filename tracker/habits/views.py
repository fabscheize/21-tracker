import django.contrib.auth
import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views
import django.views.generic

import habits.forms
import habits.models

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
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
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
        if habit.day_count < habit.count:
            habit.day_count += 1
            habit.save()

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
        habit = form.save(commit=False)
        habit.user = self.request.user
        count = form.cleaned_data.get(
            habits.models.Habits.count.field.name,
        )
        if count < habit.day_count:
            habit.day_count = count

        habit.save()

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
        habit.day_count = 0
        habit.save()
        return django.shortcuts.redirect(
            django.urls.reverse_lazy("habits:list"),
        )
