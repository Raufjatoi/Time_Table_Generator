from django import forms 
from django.contrib.auth.models import User
from .models import Teacher, Subject, SubjectGroup, SubjectGroupMapping, Department, Day , Break


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username' , 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'specialization', 'email', 'phone']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher' , 'type']

class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = ['name']

class SubjectGroupMappingForm(forms.ModelForm):
    class Meta:
        model = SubjectGroupMapping
        fields = ['group', 'subject']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['full_name', 'short_name', 'year', 'major_subjects', 'minor_subjects']

class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['day_name']
    
class BreakForm(forms.ModelForm):
    class Meta:
        model = Break
        fields = ['start_time', 'end_time']