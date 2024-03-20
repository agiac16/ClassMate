from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from assignments.models import Assignment
from courses.models import Course
from users.models import Student
from .forms import AssignmentForm, CourseForm
from django.urls import reverse

@login_required
def dashboard(request):
    student = get_object_or_404(Student, account=request.user)
    today = timezone.now().date()
    next_seven_days = [today + timedelta(days=i) for i in range(7)]
    upcoming_assignments = Assignment.objects.filter(
        student=student,  # Adjusted to reference the student
        due_date__range=(today, next_seven_days[-1])
    ).order_by('due_date')

    assignments_by_day = []
    for day in next_seven_days:
        day_assignments = [assignment for assignment in upcoming_assignments if assignment.due_date == day]
        assignments_by_day.append((day, day_assignments))

    user_courses = Course.objects.filter(enrolled_students=student)  # Adjusted to reference the student

    context = {
        'assignments_by_day': assignments_by_day,
        'user_courses': user_courses,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def course_dashboard(request, course_id):
    today = timezone.now().date()
    next_seven_days = [today + timedelta(days=i) for i in range(7)]
    
    # Make sure the course exists and the user is enrolled in it
    course = get_object_or_404(Course, id=course_id, enrolled_students=request.user)
    
    upcoming_assignments = Assignment.objects.filter(
        user=request.user,
        course=course,  # Filter by the specific course
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
        'user_courses': user_courses,  # Provide the list of user's courses for the submenu
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def add_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            return redirect(reverse('dashboard'))
    else:
        form = AssignmentForm()
    return render(request, 'dashboard/add_assignment.html', {'form': form})

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # Save the course but don't commit it to the database yet
            new_course = form.save(commit=False)
            new_course.save()
            # Now that the course is saved and has an ID, we can add enrolled students
            new_course.enrolled_students.add(request.user)
            # Ensure we save the M2M relationship change
            new_course.save()
            return redirect(reverse('dashboard'))
    else:
        form = CourseForm()
    return render(request, 'dashboard/add_course.html', {'form': form})
