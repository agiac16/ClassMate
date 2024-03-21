from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.models import Student
from courses.models import Course

@login_required
def viewProfile(request):
    student = get_object_or_404(Student, account=request.user)
    user_courses = Course.objects.filter(enrolled_students=student)
    context = {
        'user_courses': user_courses,
    }
    return render(request, 'users/profile.html', context)

@login_required
def updateProfile(request):
    if request.method == 'POST':
        user = request.user
        student = get_object_or_404(Student, user=user)

        # Log or print to ensure data is received
        print("Received data:", request.POST)

        # Update process
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()

        student.major = request.POST.get('major', student.major)
        student.enrollment_year = request.POST.get('enrollment_year', student.enrollment_year)
        student.graduation_year = request.POST.get('graduation_year', student.graduation_year)
        student.save()

        # Ensure this path is correct and only includes the necessary partial
        return render(request, 'users/profile.html', {'user': user})
