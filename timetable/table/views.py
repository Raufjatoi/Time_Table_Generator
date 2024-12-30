from django.shortcuts import render , redirect
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.decorators import login_required
from .forms import TeacherForm, SubjectForm, DepartmentForm, TimeslotForm
from .models import Teacher, Subject, Department, Timeslot, TimeTable
from .logic import is_teacher_available, is_duration_fits

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
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "teacher":
            form = TeacherForm(request.POST)
        elif form_type == "subject":
            form = SubjectForm(request.POST)
        elif form_type == "department":
            form = DepartmentForm(request.POST)
        elif form_type == "timeslot":
            form = TimeslotForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            form.save()
            return redirect("data_entry")

    context = {
        "teacher_form": TeacherForm(),
        "subject_form": SubjectForm(),
        "department_form": DepartmentForm(),
        "timeslot_form": TimeslotForm(),
    }
    return render(request, "data_entry.html", context)

def generate_timetable(request):
    if request.method == "POST":
        # Generate the timetable based on the saved data
        timetable = []
        teachers = Teacher.objects.all()
        subjects = Subject.objects.all()
        timeslots = Timeslot.objects.all()
        departments = Department.objects.all()

        for teacher in teachers:
            for subject in subjects.filter(teacher=teacher):
                for timeslot in timeslots:
                    if is_teacher_available(teacher, timeslot) and is_duration_fits(timeslot, subject):
                        timetable.append(
                            TimeTable.objects.create(
                                subject=subject,
                                department=departments.filter(subjects=subject).first(),
                                timeslot=timeslot
                            )
                        )
        return render(request, 'generate_success.html', {'timetable': timetable})

    return render(request, 'g.html')


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