from django.shortcuts import get_object_or_404, render

from courses.models import Course
from users.models import Student

# Create your views here.

def weeklyPlanner(request):
    return render(request, 'planner/weeklyCalendar.html')

def monthlyPlanner(request): 
    return render(request, 'planner/monthlyCalendar.html')
