from django import forms 
from django.contrib.auth.models import User
from .models import Teacher, Subject, SubjectGroup, SubjectGroupMapping, Department, Day

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
        fields = '__all__'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = '__all__'

class SubjectGroupMappingForm(forms.ModelForm):
    class Meta:
        model = SubjectGroupMapping
        fields = '__all__'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = '__all__'

