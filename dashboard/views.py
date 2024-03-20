from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from assignments.models import Assignment
from courses.models import Course
from users.models import Student

def dashboard(request):
    today = timezone.now().date()
    next_seven_days = [today + timedelta(days=i) for i in range(7)]
    upcoming_assignments = Assignment.objects.filter(
        user=request.student.user,
        due_date__range=(today, next_seven_days[-1])
    ).order_by('due_date')

    assignments_by_day = []
    for day in next_seven_days:
        day_assignments = [assignment for assignment in upcoming_assignments if assignment.due_date == day]
        assignments_by_day.append((day, day_assignments))

    # Fetch courses for the logged-in user correctly
    user_courses = Course.objects.filter(enrolled_students=request.user)

    context = {
        'assignments_by_day': assignments_by_day,
        'user_courses': user_courses,  # Corrected user_courses query
    }
    print(user_courses)
    return render(request, 'dashboard.html', context)