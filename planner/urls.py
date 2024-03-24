from django.views.generic import TemplateView
from django.conf.urls import include
from django.urls import re_path

from django.contrib import admin
from django.conf import settings

from planner.models.calendars import Calendar
from planner.periods import Day, Month, Week, Year
from planner.views import CalendarByPeriodsView


admin.autodiscover()

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name="homepage.html"),),
    # path(r'^planner/', include('planner.urls')),
    re_path(r'^fullcalendar/', TemplateView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),
    # path(r'^admin/', admin.site.urls),
    re_path(
        r"^calendar/month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="planner/calendar_month.html"),
        name="month_calendar",
        kwargs={"period": Month},
    ),
    re_path(
        r"^calendar/week/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="planner/calendar_week.html"),
        name="week_calendar",
        kwargs={"period": Week},
    ),
]