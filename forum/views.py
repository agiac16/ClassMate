from django.shortcuts import get_object_or_404, render

from .models import Student
from .models import Course  # assuming you have a Course model in your models.py

# lists all the courses.. page or in sidebar?
def courseList(request): 
    return render(request, 'forum/forums.html')

# after course clicked, takes you to forum
# display all posts in time order, newest first
def courseForum(request, course_id): 
    return render(request, 'forum/courseForum.html', {'course_id': course_id})

# allows you to see the post and its info
def postDetail(request, course_id, post_id): 
    return render(request, 'forum/forumPost.html', {'course_id': course_id, 'post_id': post_id})
