from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
    path('weekly/', views.weeklyPlanner, name='weekly'),
    path('monthly/', views.monthlyPlanner, name='monthly'),
]