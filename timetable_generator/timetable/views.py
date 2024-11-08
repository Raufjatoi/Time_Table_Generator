from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfessorForm, SubjectForm, TimeSlotForm
from .models import Subject, TimeSlot

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Professor.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('timetable-home')
    else:
        form = UserRegisterForm()
    return render(request, 'timetable/register.html', {'form': form})

@login_required
def timetable_home(request):
    subjects = Subject.objects.all()
    time_slots = TimeSlot.objects.all()
    return render(request, 'timetable/home.html', {'subjects': subjects, 'time_slots': time_slots})

@login_required
def add_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save(commit=False)
            professor.user = request.user
            professor.save()
            return redirect('timetable-home')
    else:
        form = ProfessorForm()
    return render(request, 'timetable/add_professor.html', {'form': form})

@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable-home')
    else:
        form = SubjectForm()
    return render(request, 'timetable/add_subject.html', {'form': form})

@login_required
def add_time_slot(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable-home')
    else:
        form = TimeSlotForm()
    return render(request, 'timetable/add_time_slot.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'timetable/profile.html')