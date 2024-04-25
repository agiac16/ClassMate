from django.shortcuts import render, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from assignments.models import Assignment
from django.db.models import Q
from users.models import Student
from courses.models import Course, Rule
from django.utils import timezone
import datetime
import pytz
import json


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

    # Create a dictionary to store assignments organized by day
    studentUserCourses = {}
    user_courses = Course.objects.filter(enrolled_students=student)
    for course in user_courses:
        # Initialize an empty list if the key doesn't exist
        if course.crn not in studentUserCourses:
            studentUserCourses[course.crn] = []

        # Convert time objects to string representation
        start_time_str = course.start_time.strftime('%H:%M:%S')
        end_time_str = course.end_time.strftime('%H:%M:%S')

        # default to spring 2024 start and end dates
        start_date_str = '2024-01-10'  # Replace with your actual start date
        end_date_str = '2024-05-03'    # Replace with your actual end date  

        # Combine date and time strings into ISO8601 format with timezone UTC-05:00
        start_datetime = datetime.datetime.strptime(f'{start_date_str} {start_time_str}', '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=5)
        end_datetime = datetime.datetime.strptime(f'{end_date_str} {end_time_str}', '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=5)

        studentUserCourses[course.crn].append({
            'title': course.course_name,
            'start': start_date_str,
            'end': end_date_str,
            'start_datetime':start_datetime.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
            'end_datetime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
            'rule_freq': course.rule.frequency,
            'rule_name':course.rule.name,
            'byweekday':course.rule.params,
            'starttime':start_time_str,
            'endtime':end_time_str,
        })  
    # user_courses = Course.objects.filter(enrolled_students=student)
    user_courses_json = json.dumps(studentUserCourses)

    context = {
        'assignments_by_day_json': assignments_by_day_json,
        'user_courses': user_courses_json,
        'userCoursesSidebar': user_courses,
    }
    return render(request, 'planner/monthlyCalendar.html', context)
