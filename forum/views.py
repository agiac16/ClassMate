from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Course, ForumPost, ForumThread, Student
from .forms import ForumPostForm
from notifications.signals import notify


def courseList(request):
    student = get_object_or_404(Student, account=request.user)
    courses = Course.objects.filter(enrolled_students=student)
    return render(request, 'forum/forums.html', {'courses': courses})

def get_course_posts(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    posts = ForumPost.objects.filter(course=course).values('id', 'title', 'content', 'posted_by__account__username', 'timestamp')
    return JsonResponse({'posts': list(posts)})

def get_replies(request, post_id):
    replies = ForumThread.objects.filter(parent_post_id=post_id).values(
        'id', 'content', 'posted_by__account__username', 'timestamp'
    ).order_by('timestamp')  # Ensure replies are ordered by timestamp
    return JsonResponse({'replies': list(replies)})

 
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


                return JsonResponse({'success': True, 'post': {
                        'id': new_post.id,
                        'title': new_post.title,
                        'content': new_post.content,
                        'posted_by__account__username': request.user.username, # Modify as needed based on your user model
                        'timestamp': new_post.timestamp.strftime('%Y-%m-%d %H:%M:%S'), # Format timestamp as you need
                    }})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid course ID'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})




def create_reply(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            parent_post = get_object_or_404(ForumPost, id=post_id)
            reply = ForumThread.objects.create(
                parent_post=parent_post,
                content=content,
                posted_by=request.user.student  # Assuming a Student model is related to User
            )
            return JsonResponse({'success': True, 'reply_id': reply.id})
        else:
            return JsonResponse({'success': False, 'errors': 'Content cannot be empty'})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})


from django.views.decorators.http import require_POST

@require_POST
def edit_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    if post.posted_by != request.user.student:
        return JsonResponse({'success': False, 'errors': 'You do not have permission to edit this post.'})

    content = request.POST.get('content')
    if content:
        post.content = content
        post.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': 'Content cannot be empty'})

@require_POST
def edit_reply(request, reply_id):
    reply = get_object_or_404(ForumThread, id=reply_id)
    if reply.posted_by != request.user.student:
        return JsonResponse({'success': False, 'errors': 'You do not have permission to edit this reply.'})

    content = request.POST.get('content')
    if content:
        reply.content = content
        reply.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': 'Content cannot be empty'})



