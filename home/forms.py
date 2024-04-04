from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class StudentSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    enrollment_year = forms.IntegerField()
    major = forms.CharField(max_length=255)
    expected_graduation_year = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')