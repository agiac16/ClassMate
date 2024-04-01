from django.shortcuts import get_object_or_404, render

from assignments.models import Assignment
from courses.models import Course
from users.models import Student
from schedule.models import Calendar
from schedule.models import Rule
from schedule.models import Event
from django.utils import timezone
from datetime import timedelta
import datetime
import schedule

# Create your views here.

def weeklyPlanner(request):
    return render(request, 'planner/weeklyCalendar.html')

def monthlyPlanner(request): 
    print("Create Example Calendar ...")
    cal = Calendar(name="Example Calendar", slug="planner")
    # cal.save()

    rule = Rule(frequency="MONTHLY", name="Monthly", description="will recur once every Month")
    rule.save()

    # student = get_object_or_404(Student, account=request.user)
    today = timezone.now().date()
    # next_thirty_days = [today + timedelta(days=i) for i in range(0, 30)]
    # upcoming_assignments = Assignment.objects.filter(
    #     student=student,  # Adjusted to reference the student
    #     due_date__range=(today, next_thirty_days[-1])
    # ).order_by('due_date')

    # assignments_by_day = []
    # for day in next_thirty_days:
    #     day_assignments = [assignment for assignment in upcoming_assignments if assignment.due_date == day]
    #     assignments_by_day.append((day, day_assignments))

    # user_courses = Course.objects.filter(enrolled_students=student)  # Adjusted to reference the student

    # start = datetime.datetime(today.year, 11, 5, 15, 0)
    # end = datetime.datetime(today.year, 11, 5, 16, 30)
    # data = {
    #     'title': 'Exercise',
    #     'start': start,
    #     'end': end,
    #     'end_recurring_period': datetime.datetime(today.year + 20, 6, 1, 0, 0),
    #     'rule': rule,
    #     'calendar': cal
    # }
    # event = Event(**data)
    # event.save()

    # event_list = schedule.settings.GET_EVENTS_FUNC(request, cal)
    # period = schedule.periods.Period(
    #     event_list,
    #     data,
    #     data
    # )
    # occs = period.get_occurrences()  # query with local time!!!
    # for occ in occs:
    #     print(occ.start)
    

    # context = {
    #     'assignments_by_day': assignments_by_day,
    #     'user_courses': user_courses,
    # }
    # return render(request, 'dashboard/dashboard.html', context)
    return render(request, 'planner/monthlyCalendar.html')
