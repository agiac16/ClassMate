from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


from assignments.models import Assignment
from users.models import Student
from courses.models import Course
from .forms import StudentForm


@login_required
def viewProfile(request):
    student = get_object_or_404(Student, account=request.user)
    user_courses = Course.objects.filter(enrolled_students=student)
    context = {
        'user_courses': user_courses,
    }
    #handle the saving 
    if request.method == 'GET':
        return render(request, 'users/profile.html', context)
    
    elif request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = StudentForm(data, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'partials/student-details.html', context)
        
        context['form'] = form 
        return render(request, 'partials/update-profile.html', context)
    
@login_required
def updateProfile(request):
    student = get_object_or_404(Student, account=request.user)
    form = StudentForm(instance=student) #fill out form with given user info

    context = {
        'student': student,
        'form': form
    }
    return render(request, 'partials/update-profile.html', context)

@login_required
def deleteCourse(request, pk):
    course = get_object_or_404(Course, pk=pk)
    student = get_object_or_404(Student, account=request.user)

    # Delete all assignments associated with the course for the student
    Assignment.objects.filter(course=course, student=student).delete()

    course.enrolled_students.remove(student)

    user_courses = Course.objects.filter(enrolled_students=student)

    context = {
        'user_courses': user_courses,
    }

    return render(request, 'partials/course-list.html', context)

def resetPassword(request, pk):
    context = {'pk': pk}

    return render(request, 'users/resetPassword.html/', context)