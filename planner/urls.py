from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('weekly/', views.weeklyPlanner, name='weekly'),
    path('planner/<int:year>/<int:month>/', views.generate_daily_planner, name='monthly_planner'),
]