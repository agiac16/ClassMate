from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from users.models import Student

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


# need a custom form to get other info.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Get a User instance without saving it to the database
            user.save()  # Save the User instance to the database
            Student.objects.create(account=user)  # Create a Student object for the new user
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')
