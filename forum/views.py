from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Course, ForumPost, Student
from .forms import ForumPostForm

def courseList(request):
    student = get_object_or_404(Student, account=request.user)
    courses = Course.objects.filter(enrolled_students=student)
    return render(request, 'forum/forums.html', {'courses': courses})

def get_course_posts(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    posts = ForumPost.objects.filter(course=course).values('id', 'title', 'content', 'posted_by', 'timestamp')
    return JsonResponse({'posts': list(posts)})

def create_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course_id')
            if course_id.isdigit():
                course = get_object_or_404(Course, id=course_id)
                new_post = form.save(commit=False)
                new_post.course = course
                new_post.posted_by = request.user.student  # Assuming a Student model is related to User
                new_post.save()
                return JsonResponse({'success': True, 'post_id': new_post.id})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid course ID'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})
