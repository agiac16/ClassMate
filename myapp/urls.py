from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-assignment/', views.add_assignment, name='add_assignment'),  # New path for adding an assignment
    path('add-course/', views.add_course, name='add_course'),  # New path for adding a course
]