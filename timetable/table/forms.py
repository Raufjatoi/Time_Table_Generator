from django import forms 
from django.contrib.auth.models import User
from .models import Teacher, Subject, Department, Timeslot , TimeTable
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username' , 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TimeslotForm(forms.ModelForm):
    class Meta:
        model = Timeslot
        fields = ['day', 'start_time', 'end_time']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'lectures_per_week', 'duration_per_lecture', 'is_major']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'working_hours', 'available_time_slots', 'subjects']
        widgets = {
            'available_time_slots': forms.CheckboxSelectMultiple(),
            'subjects': forms.CheckboxSelectMultiple(),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'year', 'semester', 'teachers', 'major_subjects', 'minor_subjects', 'total_lectures_per_week', 'start_time', 'end_time']
        widgets = {
            'teachers': forms.CheckboxSelectMultiple(),
            'major_subjects': forms.CheckboxSelectMultiple(),
            'minor_subjects': forms.CheckboxSelectMultiple(),
        }

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['department', 'subject', 'timeslot', 'year_group', 'semester']