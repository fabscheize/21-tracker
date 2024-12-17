import calendar
import datetime

import django.utils.html
import django.views.generic

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

        completed_dates = statistic.models.HabitLog.objects.filter(
            habit__user=self.request.user,
            date__year=year,
            date__month=month,
            progress=100,
        ).values_list("date", flat=True)

        today_completed = datetime.date.today() in completed_dates

        cal = CustomHTMLCalendar(completed_dates, today_completed)
        calendar_html = cal.formatmonth(year, month)

        context.update(
            {
                "calendar": calendar_html,
                "month_year": current_month_year,
            },
        )
        return context


class CustomHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, completed_dates, today_completed):
        super().__init__(firstweekday=0)
        self.completed_dates = set(completed_dates)
        self.today_completed = today_completed

    def formatweekday(self, day):
        """Отображение короткого названия дня недели."""
        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        return f"<th class='text-center'>{weekdays[day]}</th>"

    def formatweekheader(self):
        """Форматирование заголовков дней недели."""
        return (
            "<tr>"
            + "".join(self.formatweekday(day) for day in self.iterweekdays())
            + "</tr>"
        )

    def formatday(self, day, weekday):
        """Форматирование отдельного дня с учетом стилей."""
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
        """Форматирование месяца без заголовка."""
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
