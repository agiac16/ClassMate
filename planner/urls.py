from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('planner/<int:year>/<int:month>/', views.generate_monthly_planner, name='generate_monthly_planner'),
    path('generate-planner/', views.generate_planner, name='generate_planner'),
    path('complete-assignment/<int:assignment_id>/<int:timeslot_id>/', views.complete_assignment, name='complete_assignment'),
    path('cancel-timeslot/<int:timeslot_id>/', views.cancel_timeslot, name='cancel_timeslot'),
]