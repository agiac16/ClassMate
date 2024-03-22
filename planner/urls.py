from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('weekly/', views.weeklyPlanner, name='weekly'),
    path('monthly/', views.monthlyPlanner, name='monthly'),
]