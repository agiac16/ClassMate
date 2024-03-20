from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name='dashboard'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-assignment/', views.add_assignment, name='add_assignment'),
]