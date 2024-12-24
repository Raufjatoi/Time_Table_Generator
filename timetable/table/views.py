from django.shortcuts import render , redirect
from .forms import UserRegistrationForm , UserLoginForm  , TeacherForm , SubjectForm , SubjectGroupForm , SubjectGroupMappingForm , DepartmentForm , DayForm
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from .models import Teacher, Subject, SubjectGroup, SubjectGroupMapping, Department, Day

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form' : form})

def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return redirect('login')
    return render(request , 'home.html')

def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username , password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request , 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request , 'profile.html')

@login_required
def data(request):
    forms = DepartmentForm() , TeacherForm() , SubjectForm() , SubjectGroupForm() , SubjectGroupMappingForm() , DayForm()
    return render(request , 'data.html' , {'forms': forms})

@login_required
def generate(request):
    data = Department.objects.all()
    if not data:
        return redirect('data')
    else:
        return render(request , 'generate.html')