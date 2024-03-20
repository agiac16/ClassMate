from django import forms
from django.forms import ModelForm, Textarea, SelectDateWidget, NumberInput
from assignments.models import Assignment
from courses.models import Course


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'priority', 'estimated_completion_time']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': SelectDateWidget(attrs={'class': 'form-control date-picker'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': 1, 'max': 5, 'step': 1}),
            'estimated_completion_time': forms.TextInput(attrs={'class': 'form-control'}),  # Use TextInput for manual duration entry
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'crn', 'department', 'credit_hours', 'description']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'crn': NumberInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_hours': NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }