from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from users.models import Student
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def homepage(request):
    return render(request, 'home/homepage.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:dashboard')  # Redirect to the dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})


class StudentSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    enrollment_year = forms.IntegerField()
    major = forms.CharField(max_length=255)
    expected_graduation_year = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

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
        form = StudentSignUpForm()
    return render(request, 'home/signup.html', {'form': form})

def logout_view(request):
        logout(request) # Logout the user
        return redirect('login') # Redirect to login