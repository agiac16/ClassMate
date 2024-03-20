from django.shortcuts import render

def homepage(request):
    return render(request, 'home/homepage.html')

def signup(request):
    return render(request, 'home/signup.html')

def login(request):
    return render(request, 'home/login.html')