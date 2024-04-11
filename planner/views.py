from django.shortcuts import render
from schedule.models import Event

# Create your views here.

def weeklyPlanner(request):
    return render(request, 'planner/weeklyCalendar.html')

def monthlyPlanner(request): 
    events = Event.objects.all()
    return render(request, 'planner/monthlyCalendar.html', {'events': events})
