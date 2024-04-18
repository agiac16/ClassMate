from django import template
register = template.Library()

@register.simple_tag
def get_timeslots(planner, date):
    return planner.timeslot_set.filter(date=date)