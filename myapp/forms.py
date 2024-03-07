from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Assignment, Course
from django.forms.widgets import SelectDateWidget, NumberInput, Textarea

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'priority', 'estimated_completion_time']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': SelectDateWidget(attrs={'class': 'form-control date-picker'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': 1, 'max': 5}),
            'estimated_completion_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'department', 'credit_hours', 'description']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_hours': NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
