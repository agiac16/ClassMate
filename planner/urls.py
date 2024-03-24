from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
from django.conf import settings

from planner.models import Calendar
from planner.periods import Day, Month, Week, Year
from planner.views import (
    CalendarByPeriodsView,
    CalendarView,
    CancelOccurrenceView,
    CreateEventView,
    CreateOccurrenceView,
    DeleteEventView,
    EditEventView,
    EditOccurrenceView,
    EventView,
    FullCalendarView,
    OccurrencePreview,
    OccurrenceView,
    api_move_or_resize_by_code,
    api_occurrences,
    api_select_create,
)


admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="homepage.html"),),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^fullcalendar/', TemplateView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),
    url(r'^admin/', admin.site.urls),
    path(
        r"^calendar/month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_month.html"),
        name="month_calendar",
        kwargs={"period": Month},
    ),
    path(
        r"^calendar/week/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_week.html"),
        name="week_calendar",
        kwargs={"period": Week},
    ),
]