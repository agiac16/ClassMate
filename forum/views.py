from django.shortcuts import get_object_or_404, render

from .models import Student
from .models import Course  # assuming you have a Course model in your models.py

# lists all the courses.. page or in sidebar?
def courseList(request): 
    student = get_object_or_404(Student, account=request.user)
    courses = Course.objects.filter(enrolled_students=student) #so the courses can be viewed in nav

    return render(request, 'forum/forums.html', {'courses': courses})

# after course clicked, takes you to forum
# display all posts in time order, newest first
def courseForum(request, course_id): 
    return render(request, 'forum/courseForum.html', {'course_id': course_id})

# allows you to see the post and its info
def postDetail(request, course_id, post_id): 
    return render(request, 'forum/forumPost.html', {'course_id': course_id, 'post_id': post_id})

# TODO:
# - Fix all HTML, extend from core sidebar