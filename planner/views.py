from django.shortcuts import render, get_object_or_404
from schedule.models import Event
from assignments.models import Assignment
from django.db.models import Q
from users.models import Student


# Create your views here.

def weeklyPlanner(request):
    return render(request, 'planner/weeklyCalendar.html')

def monthlyPlanner(request): 
    student = get_object_or_404(Student, account=request.user)

    # Retrieve all assignments from the database
    assignments = Assignment.objects.filter(
        Q(students=student) | Q(owner=student)).order_by('due_date')  # Include assignments where the student is the owner

    # Create a dictionary to store assignments organized by day
    assignments_by_day = {}

    # Iterate through assignments and organize them by day
    for assignment in assignments:
        due_date = assignment.due_date  # Get the date part of the due date
        # Check if the due date already exists in assignments_by_day
        if due_date in assignments_by_day:
            assignments_by_day[due_date].append(assignment)
        else:
            assignments_by_day[due_date] = [assignment]

    # Sort assignments_by_day by date
    sorted_assignments_by_day = dict(sorted(assignments_by_day.items()))

    # Pass the organized data to the template
    context = {
        'assignments_by_day': sorted_assignments_by_day
    }

    return render(request, 'planner/monthlyCalendar.html', context)
