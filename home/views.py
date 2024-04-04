from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from users.models import Student
from .forms import StudentSignUpForm, AuthenticationForm

def homepage(request):
    return render(request, 'home/homepage.html')

def contact(request):
    return render(request, 'home/contact.html')

def faq(request):
    return render(request, 'home/faq.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:dashboard')  # Redirect to the dashboard
    else:
        if request.user.is_authenticated:
            return redirect('homepage')
        form = AuthenticationForm()
    
    return render(request, 'home/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(
                account=user,
                full_name=form.cleaned_data.get('full_name'),
                enrollment_year=form.cleaned_data.get('enrollment_year'),
                major=form.cleaned_data.get('major'),
                expected_graduation_year=form.cleaned_data.get('expected_graduation_year')
            )
            login(request, user)
            return redirect('dashboard:dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('homepage')
        form = StudentSignUpForm()
        return render(request, 'home/signup.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request) # Logout the user
        return redirect('login') # Redirect to login
    return redirect('homepage')