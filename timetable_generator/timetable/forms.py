from django import forms
from django.contrib.auth.models import User
from .models import Professor, Subject, TimeSlot

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['specialization']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'department', 'professor']

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['day', 'start_time', 'end_time']
