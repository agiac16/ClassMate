from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from django.utils import timezone
from .models import Assignment
from .forms import AssignmentForm
from .forms import CourseForm
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    # Get today's date and the end date of the current week
    today = timezone.now().date()
    end_of_week = today + timedelta(days=6 - today.weekday())  # Adjusted to get the end of the current week

    # Fetch assignments for the current week for the logged-in user
    upcoming_assignments = Assignment.objects.filter(
        user=request.user,
        due_date__range=(today, end_of_week)
    ).order_by('due_date')

    # Organize assignments by day
    assignments_by_day = {}
    for assignment in upcoming_assignments:
        if assignment.due_date not in assignments_by_day:
            assignments_by_day[assignment.due_date] = []
        assignments_by_day[assignment.due_date].append(assignment)

    context = {
        'assignments_by_day': sorted(assignments_by_day.items())
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            return redirect(reverse('dashboard'))
    else:
        form = AssignmentForm()
    return render(request, 'add_assignment.html', {'form': form})
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})
