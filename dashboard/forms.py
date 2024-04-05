from django import forms
from django.forms import ModelForm, Textarea, SelectDateWidget, NumberInput, Select
from assignments.models import Assignment
from courses.models import Course
from users.models import Student
from django.shortcuts import get_object_or_404


class AssignmentForm(forms.ModelForm):
    student_username = forms.CharField(
        max_length=150,
        required=False  # Make this field optional
    )

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'student_username', 'due_date', 'priority']  # Added 'student_username'
        widgets = {
            'course': forms.Select(attrs={'class': 'mt-2 mb-2 py-4 px-6 bg-white rounded-xl'}),
            'title': forms.TextInput(attrs={'class': 'mt-2 mb-2 py-4 px-6 bg-white rounded-xl'}),
            'description': Textarea(attrs={'class': 'mt-2 mb-2 py-4 px-6 bg-white rounded-xl', 'rows': 3}),
            'due_date': SelectDateWidget(attrs={'class': 'w-full mt-2 mb-2 py-4 px-6 bg-white rounded-xl date-picker'}),
            'priority': forms.NumberInput(attrs={'class': 'w-full mt-2 mb-2 py-4 px-6 bg-white rounded-xl', 'type': 'range', 'min': 1, 'max': 5, 'step': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        student_username = cleaned_data.get('student_username')

        if student_username:
            try:
                additional_student = Student.objects.get(account__username=student_username)
                if course not in additional_student.enrolled_courses.all():
                    self.add_error('student_username', 'This student is not enrolled in the selected course.')
            except Student.DoesNotExist:
                self.add_error('student_username', 'No student found with this username')

        # Check if the owner is enrolled in the selected course
        if self.user:
            owner = Student.objects.get(account=self.user)
            if course not in owner.enrolled_courses.all():
                self.add_error('course', 'You are not enrolled in the selected course.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the 'user' argument
        super(AssignmentForm, self).__init__(*args, **kwargs)
        if self.user is not None:
            student = get_object_or_404(Student, account=self.user)
            self.fields['course'].queryset = student.enrolled_courses.all()
        if self.instance.id and self.instance.students.exists():  # Check self.instance.id before accessing students
            self.fields['student_username'].initial = self.instance.students.first().account.username

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'crn', 'department', 'credit_hours']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'crn': NumberInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_hours': NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
        }