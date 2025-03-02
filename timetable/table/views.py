from django.shortcuts import render , redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from .forms import TeacherForm, SubjectForm, DepartmentForm, TimeslotForm
from .models import Teacher, Subject, Department, Timeslot, TimeTable
from .logic import *
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.urls import reverse


from.forms import UserRegistrationForm , UserLoginForm
def register(request):
    error_message = None  
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('profile')
        else:
            error_message = "Try again please 🥺"
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'error': error_message})

def home(request):
    if request.user.is_authenticated:
        return render(request , 'home.html')
    else:
        return redirect('login')

def login_view(request):
    error_message = None 
    form = UserLoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')  
        else:
            error_message = "Try again 🙂, password or username was incorrect ig :("
    
    return render(request, 'login.html', {'form': form, 'error': error_message})
def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request , 'profile.html')

def data_entry(request):
    return render(request , 'data_entry.html')

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()  # save the form data to the database
            success_message = "Teacher added 👨‍🏫"
            return redirect('data_entry')  # If no parameters needed
  
        else:
            error_message = "Form data is invalid. Please check your again"
    else:
        form = TeacherForm()
        error_message = None  

    return render(request, 'add_teacher.html', {'form': form, 'error': error_message})



def generate_timetable(request):
    timetable = {}

    # Fetch all departments
    for department in Department.objects.all():
        department_timetable = []

        # Fetch all subjects
        subjects = list(department.major_subjects.all()) + list(department.minor_subjects.all())

        # Fetch available teachers
        teachers = {subject: subject.assigned_teachers.all() for subject in subjects}

        # Fetch available time slots
        time_slots = Timeslot.objects.all()

        slot_index = 0
        for subject in subjects:
            if slot_index >= len(time_slots):
                break  # Stop if out of time slots
            
            timeslot = time_slots[slot_index]
            slot_index += 1

            # Assign a teacher (if available)
            available_teachers = teachers.get(subject, [])
            teacher = available_teachers[0] if available_teachers else "No Teacher"

            department_timetable.append({
                "timeslot": timeslot,
                "subject": subject.name,
                "teacher": teacher if teacher == "No Teacher" else teacher.name
            })

        timetable[department.name] = department_timetable

    return render(request, 'timetable.html', {"timetable": timetable})


def doc(request):
    return render(request , 'doc.html')

def works(request):
    return render(request , 'works.html')

def us(request):
    return render(request , 'us.html')

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()  # save the form data to the database
            success_message = "Subject added 📕"
            return HttpResponseRedirect(f"{reverse('data_entry')}?success={success_message}")
        else:
            error_message = "Form data is invalid. Please check your again"
    else:
        form = SubjectForm()
        error_message = None  

    return render(request, 'add_subject.html', {'form': form, 'error': error_message})


def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()  # save the form data to the database
            success_message = "Department added 🏢"
            return HttpResponseRedirect(f"{reverse('data_entry')}?success={success_message}")  
        else:
            error_message = "Form data is invalid. Please check your again"
    else:
        form = DepartmentForm()
        error_message = None  

    return render(request, 'add_department.html', {'form': form, 'error': error_message})


def add_timeslot(request):
    if request.method == 'POST':
        form = TimeslotForm(request.POST)
        if form.is_valid():
            form.save()  # save the form data to the database
            success_message = "timeslot added 🕒"
            return HttpResponseRedirect(f"{reverse('data_entry')}?success={success_message}")
        else:
            error_message = "Form data is invalid. Please check your again"
    else:
        form = TimeslotForm()
        error_message = None  

    return render(request, 'add_timeslot.html', {'form': form, 'error': error_message})


@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return render(request, 'change_password.html', {'error': "Passwords do not match :( "})
        
        user = request.user
        if not user.check_password(old_password):
            return render(request, 'change_password.html', {'error': "Old password is incorrect : ("})
        
        user.set_password(new_password)
        user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, user)
        
        return redirect('login') 
    
    return render(request, 'change_password.html')


'''
def generate_timetable():
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    timeslots = Timeslot.objects.all()
    departments = Department.objects.all()

    for department in departments:
        for subject in subjects.filter(department=department):
            for teacher in subject.teachers.all():
                for timeslot in timeslots:
                    # Check all conditions
                    if (
                        is_teacher_available(teacher, timeslot) and
                        is_teacher_under_working_hours(teacher, timeslot) and
                        is_subject_under_lectures_per_week(subject) and
                        is_duration_fits(timeslot, subject) and
                        is_department_available(department, timeslot) and
                        is_department_under_working_hours(department, timeslot) and
                        is_department_under_lectures_per_week(department, subject) and
                        is_subject_in_department(department, subject)
                    ):
                        # Create a timetable entry if all conditions are satisfied
                        TimeTable.objects.create(
                            subject=subject,
                            teacher=teacher,
                            timeslot=timeslot,
                            department=department
                        )
                        break
'''