from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.courseList, name='courseList'),
   
    path('course/<int:course_id>/posts/', views.get_course_posts, name='get_course_posts'),
    path('create_post/', views.create_post, name='create_post'), 
    path('post/<int:post_id>/create_reply/', views.create_reply, name='create_reply'),
    path('post/<int:post_id>/replies/', views.get_replies, name='get_replies'),

   
]

