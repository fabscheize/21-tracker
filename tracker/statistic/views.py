import calendar
import datetime

import django.shortcuts
import django.utils.html
import django.views.generic

import habits.models
import statistic.models

__all__ = ()


class ProgressView(django.views.generic.TemplateView):
    template_name = "statistic/progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = datetime.date.today().year
        month = datetime.date.today().month
        current_month_year = (
            datetime.date.today().strftime("%B %Y").capitalize()
        )

        user_habits = habits.models.Habits.objects.filter(
            user=self.request.user,
        )
        selected_habit_id = self.request.GET.get("habit")
        selected_habit = None

        if selected_habit_id:
            selected_habit = django.shortcuts.get_object_or_404(
                habits.models.Habits,
                id=selected_habit_id,
                user=self.request.user,
            )

        if selected_habit:
            completed_dates = statistic.models.HabitLog.objects.filter(
                habit=selected_habit,
                date__year=year,
                date__month=month,
                progress=100,
            ).values_list("date", flat=True)
        else:
            completed_dates = self.get_days_all_habits_completed(
                user_habits,
                year,
                month,
            )

        today_completed = datetime.date.today() in completed_dates
        cal = CustomHTMLCalendar(completed_dates, today_completed)
        calendar_html = cal.formatmonth(year, month)

        weekly_progress_with_dates = self.calculate_weekly_progress(
            self.request.user,
            selected_habit,
        )

        context.update(
            {
                "calendar": calendar_html,
                "month_year": current_month_year,
                "habits": user_habits,
                "selected_habit": selected_habit,
                "weekly_progress_with_dates": weekly_progress_with_dates,
            },
        )
        return context

    def get_days_all_habits_completed(self, user_habits, year, month):
        if not user_habits.exists():
            return []

        days_in_month = [
            datetime.date(year, month, day)
            for day in range(1, calendar.monthrange(year, month)[1] + 1)
        ]
        completed_dates = []

        logs = statistic.models.HabitLog.objects

        for day in days_in_month:
            all_completed = all(
                logs.filter(
                    habit=habit,
                    date=day,
                    progress=100,
                ).exists()
                for habit in user_habits
            )
            if all_completed:
                completed_dates.append(day)

        return completed_dates

    def calculate_weekly_progress(self, user, habit):
        today = datetime.date.today()
        weekly_progress = []
        week_dates = []

        for i in range(4):
            week_start = today - datetime.timedelta(
                days=today.weekday() + i * 7,
            )
            week_end = week_start + datetime.timedelta(days=6)
            week_dates.append((week_start, week_end))

            logs = statistic.models.HabitLog.objects.filter(
                habit__user=user,
                date__range=[week_start, week_end],
            )
            if habit:
                logs = logs.filter(habit=habit)

            total_progress = sum(log.progress for log in logs)
            progress_count = logs.count()
            average_progress = (
                round(total_progress / progress_count)
                if progress_count > 0
                else 0
            )

            weekly_progress.append(average_progress)

        return list(zip(reversed(weekly_progress), reversed(week_dates)))


class CustomHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, completed_dates, today_completed):
        super().__init__(firstweekday=0)
        self.completed_dates = set(completed_dates)
        self.today_completed = today_completed

    def formatweekday(self, day):
        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        return f"<th class='text-center'>{weekdays[day]}</th>"

    def formatweekheader(self):
        return (
            "<tr>"
            + "".join(self.formatweekday(day) for day in self.iterweekdays())
            + "</tr>"
        )

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="calendar-cell empty"></td>'

        current_date = datetime.date.today().replace(day=day)
        day_content = str(day)
        cell_class = "calendar-cell"

        if (
            current_date in self.completed_dates
            and current_date == datetime.date.today()
        ):
            cell_class += " completed-today"
        elif current_date in self.completed_dates:
            cell_class += " completed"
        elif current_date == datetime.date.today():
            cell_class += " today"

        return f"""
            <td class="{cell_class}">
                <span class="day-circle">{day_content}</span>
            </td>
        """

    def formatmonth(self, year, month, withyear=True):
        weeks = [
            self.formatweek(week)
            for week in self.monthdays2calendar(year, month)
        ]
        return (
            "<table class='calendar-table'>"
            + self.formatweekheader()
            + "".join(weeks)
            + "</table>"
        )
