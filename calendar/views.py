from django.shortcuts import render

# Create your views here.

def weeklyPlanner(request): 
    return render(request, 'weeklyCalendar.html')

def monthlyPlanner(request): 
    return render(request, 'monthlyCalendar.html')