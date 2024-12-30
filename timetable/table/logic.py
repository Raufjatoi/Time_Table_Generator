from .models import Teacher, Subject, Timeslot, Department, TimeTable
from datetime import timedelta


#if a teacher is available during a specific timeslot.
def is_teacher_available(teacher, timeslot):
    return not TimeTable.objects.filter(subject__teachers=teacher, timeslot=timeslot).exists()


# if the teacher's total scheduled hours do not exceed their working hours.
def is_teacher_under_working_hours(teacher, timeslot):
    # teacher working_hours to total minutes
    total_working_minutes = int(teacher.working_hours) * 60
    # scheduled minutes for the teacher
    total_scheduled_minutes = sum(
        timetable.subject.duration_per_lecture
        for timetable in TimeTable.objects.filter(subject__teachers=teacher)
    )
    # duration of the current timeslot
    current_duration = (timeslot.end_time - timeslot.start_time).total_seconds() / 60
    return total_scheduled_minutes + current_duration <= total_working_minutes


# if a subject has remaining lectures to be scheduled for the week.
def is_subject_under_lectures_per_week(subject):
    total_lectures = TimeTable.objects.filter(subject=subject).count()
    return total_lectures < subject.lectures_per_week


# if the subject's lecture duration fits within the given timeslot.
def is_duration_fits(timeslot, subject):
    current_duration = (timeslot.end_time - timeslot.start_time).total_seconds() / 60
    return current_duration >= subject.duration_per_lecture


#  no overlapping timeslots for the same department.
def is_department_available(department, timeslot):
    return not TimeTable.objects.filter(department=department, timeslot=timeslot).exists()


# if the department's total scheduled teaching hours fit within its operational hours.
def is_department_under_working_hours(department, timeslot):
    # total scheduled minutes for the department
    total_scheduled_minutes = sum(
        timetable.subject.duration_per_lecture
        for timetable in TimeTable.objects.filter(department=department)
    )
    # department operational minutes
    department_hours = (department.end_time - department.start_time).total_seconds() / 60
    #the current timeslot duration
    current_duration = (timeslot.end_time - timeslot.start_time).total_seconds() / 60
    return total_scheduled_minutes + current_duration <= department_hours


#department does not exceed its total lectures per week for major and minor subjects.
def is_department_under_lectures_per_week(department, subject):
    total_major_lectures = TimeTable.objects.filter(department=department, subject__is_major=True).count()
    total_minor_lectures = TimeTable.objects.filter(department=department, subject__is_major=False).count()

    if subject.is_major:
        major_quota = department.total_lectures_per_week // 2  #50/50 split for major/minor ?? or 70/30 ??
        return total_major_lectures < major_quota
    else:
        minor_quota = department.total_lectures_per_week // 2
        return total_minor_lectures < minor_quota


# subjects being scheduled align with the department's major/minor categories.
def is_subject_in_department(department, subject):
    if subject.is_major:
        return department.major_subjects.filter(pk=subject.pk).exists()
    else:
        return department.minor_subjects.filter(pk=subject.pk).exists()