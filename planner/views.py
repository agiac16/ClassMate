from django.shortcuts import render, get_object_or_404
from assignments.models import Assignment
from django.db.models import Q
from users.models import Student
import json

def weeklyPlanner(request): 
    return render(request, 'planner/weeklyCalendar.html', )
 
def monthlyPlanner(request): 
    student = get_object_or_404(Student, account=request.user)

    # Retrieve all assignments from the database
    assignments = Assignment.objects.filter(
        Q(students=student) | Q(owner=student)).order_by('due_date')  # Include assignments where the student is the owner

    # Create a dictionary to store assignments organized by day
    assignments_by_day = {}

    # Iterate through assignments and organize them by day
    for assignment in assignments:
        due_date = assignment.due_date

        # Convert due_date to string for use as dictionary key
        due_date_str = str(due_date)

        # Check if the due date already exists in assignments_by_day
        if due_date_str in assignments_by_day:
            assignments_by_day[due_date_str].append({
                'title': assignment.title,
                'description': assignment.description,
                'due_date': assignment.due_date.strftime('%Y-%m-%d'),  # Convert due_date to string in YYYY-MM-DD format
                'priority': assignment.priority,
                'estimated_completion_time': str(assignment.estimated_completion_time),
            })
        else:
            assignments_by_day[due_date_str] = [{
                'title': assignment.title,
                'description': assignment.description,
                'due_date': assignment.due_date.strftime('%Y-%m-%d'),  # Convert due_date to string in YYYY-MM-DD format
                'priority': assignment.priority,
                'estimated_completion_time': str(assignment.estimated_completion_time),
            }]

    # Sort assignments_by_day by date
    sorted_assignments_by_day = dict(sorted(assignments_by_day.items()))

    assignments_by_day_json = json.dumps(sorted_assignments_by_day)

    context = {
        'assignments_by_day_json': assignments_by_day_json
    }
    return render(request, 'planner/monthlyCalendar.html', context)
