from pyexpat.errors import messages
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from assignments.models import Assignment
from courses.models import Course
from users.models import Student
from .forms import AssignmentForm, CourseForm
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
import traceback
from notifications.models import Notification



@login_required
def dashboard(request):
    student = get_object_or_404(Student, account=request.user)
    today = timezone.now().date()
    next_thirty_days = [today + timedelta(days=i) for i in range(0, 30)]
    upcoming_assignments = Assignment.objects.filter(
        student=student,  # Adjusted to reference the student
        due_date__range=(today, next_thirty_days[-1])
    ).order_by('due_date')

    assignments_by_day = []
    for day in next_thirty_days:
        day_assignments = [assignment for assignment in upcoming_assignments if assignment.due_date == day]
        assignments_by_day.append((day, day_assignments))

    user_courses = Course.objects.filter(enrolled_students=student)  # Adjusted to reference the student

    # Add this line to define notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

    context = {
        'assignments_by_day': assignments_by_day,
        'user_courses': user_courses,
        'notifications': notifications,
        'today': today,  # Add this line to include today in the context
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def course_dashboard(request, course_id):
    student = get_object_or_404(Student, account=request.user)
    today = timezone.now().date()
    next_thirty_days = [today + timedelta(days=i) for i in range(0,30)]
    
    # Make sure the course exists and the user is enrolled in it
    course = get_object_or_404(Course, id=course_id, enrolled_students=student)
    
    upcoming_assignments = Assignment.objects.filter(
        student=student,
        course=course,  # Filter by the specific course
        due_date__range=(today, next_thirty_days[-1])
    ).order_by('due_date')

    assignments_by_day = []
    for day in next_thirty_days:
        day_assignments = [assignment for assignment in upcoming_assignments if assignment.due_date == day]
        assignments_by_day.append((day, day_assignments))
    
    user_courses = Course.objects.filter(enrolled_students=student)

    context = {
        'assignments_by_day': assignments_by_day,
        'user_courses': user_courses,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def add_assignment(request):
    student = get_object_or_404(Student, account=request.user)
    user_courses = Course.objects.filter(enrolled_students=student) #so the courses can be viewed in nav

    if request.method == 'POST':
        form = AssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = student
            assignment.owner = student  # Assign the current student as the owner
            assignment.save()
            return redirect(reverse('dashboard:dashboard'))
    else:
        form = AssignmentForm(user=request.user)
    
    return render(request, 'dashboard/add_assignment.html', {'form': form, 'user_courses': user_courses})

@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = get_object_or_404(Student, account=request.user)
    user_courses = Course.objects.filter(enrolled_students=student)

    # Ensure the user is the owner of the assignment before allowing them to edit
    if student != assignment.owner:
        return redirect('dashboard:dashboard')

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment, user=request.user)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:dashboard'))
    else:
        form = AssignmentForm(instance=assignment, user=request.user)

    return render(request, 'dashboard/edit_assignment.html', {'form': form, 'user_courses': user_courses, 'assignment': assignment})

@login_required
def add_course(request, course_id):
    student = get_object_or_404(Student, account=request.user)
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        # Add the course to the student's enrolled courses
        student.enrolled_courses.add(course)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

def search_courses(request):
    try:
        print("Request method:", request.method)
        print("Request GET parameters:", request.GET)
        
        search_query = request.GET.get('query', '')
        department_filter = request.GET.get('department_filter', '')
        credit_hours_filter = request.GET.get('credit_hours', '')


        print("Search query:", search_query)
        
        courses = Course.objects.filter(
            Q(course_name__icontains=search_query) |
            Q(crn__icontains=search_query) |
            Q(course_code__icontains=search_query),
            department__icontains=department_filter,  # Filter by department
            credit_hours__icontains=credit_hours_filter,  # Filter by credit hours
        ).values('id', 'course_name', 'crn', 'department', 'credit_hours')[:10]
        
        print("Courses queryset:", courses)
        
        return JsonResponse(list(courses), safe=False)
    except Exception as e:
        print("Error occurred:")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def add_course_page(request):
    departments = Course.objects.values_list('department', flat=True).distinct()
    student = get_object_or_404(Student, account=request.user)
    user_courses = Course.objects.filter(enrolled_students=student)
    
    context = { 
        'departments': departments,
        'user_courses': user_courses
    }

    return render(request, 'dashboard/add_course.html', context)



@login_required
def delete_assignment(request, assignment_id):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, id=assignment_id) 
        student = get_object_or_404(Student, account=request.user)

        # Ensure the user is the owner of the assignment before allowing them to delete
        if student != assignment.owner:
            messages.error(request, 'You do not have permission to delete this assignment.')
            return redirect('dashboard:dashboard')

        assignment.delete()

    return redirect('dashboard:dashboard')

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'dashboard.html', {'notifications': notifications})