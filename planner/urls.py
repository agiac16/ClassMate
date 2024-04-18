from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('planner/<int:year>/<int:month>/', views.generate_monthly_planner, name='monthly_planner'),
]