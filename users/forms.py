from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ('email', 'full_name', 'major', 'enrollment_year', 'expected_graduation_year')
        widgets = {
            'email': forms.EmailInput(attrs={
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

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.account.email

    def save(self, *args, **kwargs):
        instance = super(StudentForm, self).save(*args, **kwargs)
        instance.account.email = self.cleaned_data.get('email')