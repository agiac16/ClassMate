from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Course, ForumPost, ForumThread, Student
from .forms import ForumPostForm
from django.views.decorators.http import require_POST


@login_required
def courseList(request):
    student = get_object_or_404(Student, account=request.user)
    courses = Course.objects.filter(enrolled_students=student)
    return render(request, 'forum/forums.html', {'courses': courses, 'current_user': request.user.username})

@login_required
def get_course_posts(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    posts = ForumPost.objects.filter(course=course).values('id', 'title', 'content', 'posted_by__account__username', 'timestamp')
    return JsonResponse({
        'current_user': request.user.username,  # Add current user's username
        'posts': list(posts)
    })

@login_required
def get_replies(request, post_id):
    replies = ForumThread.objects.filter(parent_post_id=post_id).values(
        'id', 'content', 'posted_by__account__username', 'timestamp'
    ).order_by('timestamp')  # Ensure replies are ordered by timestamp
    return JsonResponse({
        'current_user': request.user.username,  # Add current user's username
        'replies': list(replies)
    })

@login_required
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
                    'posted_by__account__username': request.user.username,  # Assume username field exists
                    'timestamp': new_post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Format timestamp
                }})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid course ID'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})

@login_required
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
            return JsonResponse({'success': True, 'reply': {
                'id': reply.id,
                'content': reply.content,
                'posted_by__account__username': request.user.username,  # Add username for consistency
                'timestamp': reply.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Format timestamp
            }})
        else:
            return JsonResponse({'success': False, 'errors': 'Content cannot be empty'})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})

@require_POST
@login_required
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
@login_required
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
