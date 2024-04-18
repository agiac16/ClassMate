from django import template
from planner.models import TimeSlot

register = template.Library()

@register.simple_tag
def get_timeslots(planner, date):
    return TimeSlot.objects.filter(planner=planner, date=date).order_by('start_time')