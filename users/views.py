import curses
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from users.models import Student
from courses.models import Course



#  this will need to be tweaked to get a students ID rather than a users
# since students are diff than user

#no param pass means itll use id of current account
#@login_required
def viewProfile(request):
    # Retrieve the logged-in student based on the user account.
    student = get_object_or_404(Student, account=request.user)
    
    # Fetch the courses the student is enrolled in.
    user_courses = Course.objects.filter(enrolled_students=student)
    
    # Pass the courses to the template.
    context = {
        'user_courses': user_courses,
    }
    
    return render(request, 'users/profile.html', context)

#@login_required
def updateProfile(request):
    # Now you can use user_id to update the user's profile
    return render(request, 'users/updateProfile.html')

