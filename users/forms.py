from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student 
from schedule.models import Calendar

class StudentForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=255)
    major = forms.CharField(max_length=255)
    enrollment_year = forms.IntegerField()
    expected_graduation_year = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'major', 'enrollment_year', 'expected_graduation_year')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'bg-gray-50 pl-3',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-gray-50 pl-3',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'bg-gray-50 pl-3',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'bg-gray-50 pl-3',
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'bg-gray-50 pl-3',
            }),
            'major': forms.TextInput(attrs={
                'class': 'bg-gray-50 pl-3',
            }),
            'enrollment_year': forms.NumberInput(attrs={
                'class': 'bg-gray-50 pl-3 h-6 w-32',
            }),
            'expected_graduation_year': forms.NumberInput(attrs={
                'class': 'bg-gray-50 pl-3 h-6 w-32',
                'type': 'number',
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            student = Student.objects.create(
                account=user,
                full_name=self.cleaned_data['full_name'],
                major=self.cleaned_data['major'],
                enrollment_year=self.cleaned_data['enrollment_year'],
                expected_graduation_year=self.cleaned_data['expected_graduation_year']
            )
            calendar = Calendar.objects.create(student=student, slug=f"{user.full_name}'s Calendar")
        return user