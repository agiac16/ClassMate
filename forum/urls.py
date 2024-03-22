from django.urls import path
from . import views

urlpatterns = [

    path('', views.courseList, name='courseList'),
    path('course/<int:course_id>', views.courseForum, name='courseForum'),
    path('course/<int:course_id>/post/<int:post_id>', views.postDetail, name='postDetail'),


    
]