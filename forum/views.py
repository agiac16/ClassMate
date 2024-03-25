from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.template.loader import render_to_string
from forum.forms import ForumPostForm
from .models import Course, ForumPost
from django.http import JsonResponse

def courseList(request):
    courses = Course.objects.all()
    return render(request, 'forum/forums.html', {'courses': courses})

def get_course_posts(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
   
    posts = ForumPost.objects.filter(course=course).values('id', 'title', 'content', 'posted_by', 'timestamp')
    return JsonResponse({'posts': list(posts)})



def create_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            # Assuming you have a way to get the course, such as from a hidden field
            new_post.course_id = request.POST.get('course_id')
            new_post.save()
            # Render the new post as HTML and send it back
            html = render_to_string('partials/_post.html', {'post': new_post}, request=request)
            return JsonResponse({'html': html}, status=200)
        else:
            # If the form is not valid, send back an error status and the form errors
            return JsonResponse({'errors': form.errors}, status=400)



