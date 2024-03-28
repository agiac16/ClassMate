from pyexpat.errors import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from assignments.models import Assignment
from courses.models import Course
from users.models import Student
from .forms import AssignmentForm, CourseForm
from django.urls import reverse
from django.http import JsonResponse
import csv
from django.http import JsonResponse

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
    student = get_object_or_404(Student, account=request.user)
    today = timezone.now().date()
    next_seven_days = [today + timedelta(days=i) for i in range(7)]
    
    # Make sure the course exists and the user is enrolled in it
    course = get_object_or_404(Course, id=course_id, enrolled_students=student)
    
    upcoming_assignments = Assignment.objects.filter(
        student=student,
        course=course,  # Filter by the specific course
        due_date__range=(today, next_seven_days[-1])
    ).order_by('due_date')

    assignments_by_day = []
    for day in next_seven_days:
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
def add_course(request):
    student = get_object_or_404(Student, account=request.user)
    user_courses = Course.objects.filter(enrolled_students=student) #so the courses can be viewed in nav
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.save()
            # Now that the course is saved and has an ID, we can add enrolled students
            new_course.enrolled_students.add(student)  # Add the student instance
            new_course.save()
            return redirect(reverse('dashboard:dashboard'))
    else:
        form = CourseForm()


    return render(request, 'dashboard/add_course.html', {'form': form, 'user_courses': user_courses})

@login_required
def delete_assignment(request):
    assignment = get_object_or_404(Assignment)
    student = get_object_or_404(Student, account=request.user)

    # Ensure the user is the owner of the assignment before allowing them to delete
    if student != assignment.owner:
        messages.error(request, 'You do not have permission to delete this assignment.')
        return redirect('dashboard:dashboard')

    assignment.delete()

    return redirect('dashboard:dashboard')

@login_required
def bulk_import(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_file = request.FILES['file']
            
            # Check if the uploaded file is a CSV file
            if not uploaded_file.name.endswith('.csv'):
                return JsonResponse({'success': False, 'message': 'Invalid file format. Please upload a CSV file.'})
            
            # Decode and process the CSV file
            decoded_file = uploaded_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            
            # Read the first row to check for specific headers
            headers = next(csv_reader)
            required_headers = ['course_name', 'course_code', 'crn', 'department', 'credit_hours', 'description']
            if all(header in headers for header in required_headers):
                print("Success: All required headers found.")
                print("Headers:", headers)
                # Continue processing the file
                # You can add your processing logic here
                
                # Return success message
                return JsonResponse({'success': True, 'message': 'File uploaded successfully.'})
            else:
                missing_headers = [header for header in required_headers if header not in headers]
                return JsonResponse({'success': False, 'message': f'Missing headers: {missing_headers}'})

        except Exception as e:
            # Return error message
            return JsonResponse({'success': False, 'message': str(e)})
    
    # Return error message if no file is selected
    return JsonResponse({'success': False, 'message': 'No file selected.'})

@login_required
def add_sample_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
    else:
        form = CourseForm(initial={
            'course_name': 'Sample Course',
            'course_code': 'SAMPLE101',
            'crn': 12345,
            'department': 'Sample Department',
            'credit_hours': 3,
            'description': 'This is a sample course created for demonstration purposes.'
        })
    return redirect('dashboard:dashboard')  # Redirect to the dashboard if not a POST request