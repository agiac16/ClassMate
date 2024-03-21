from django import forms
from django.forms import ModelForm, Textarea, SelectDateWidget, NumberInput, Select
from assignments.models import Assignment
from courses.models import Course
from users.models import Student
from django.shortcuts import get_object_or_404


class AssignmentForm(forms.ModelForm):
    hours = forms.ChoiceField(choices=[(i, f"{i} hour{'s' if i != 1 else ''}") for i in range(0, 25)], widget=Select(attrs={'class': 'form-control'}))
    minutes = forms.ChoiceField(choices=[(i, f"{i} minute{'s' if i != 1 else ''}") for i in range(0, 59, 5)], widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'priority']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': SelectDateWidget(attrs={'class': 'form-control date-picker'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': 1, 'max': 5, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Correctly extract the 'user' argument
        super(AssignmentForm, self).__init__(*args, **kwargs)  # Pass the modified kwargs
        if user is not None:
            student = get_object_or_404(Student, account=user)
            self.fields['course'].queryset = Course.objects.filter(enrolled_students=student)

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