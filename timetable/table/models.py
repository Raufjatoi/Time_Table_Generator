from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    working_hours = models.CharField(max_length=100)  # working hours per day
    subjects = models.ManyToManyField('Subject', related_name='assigned_teachers')

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    lectures_per_week = models.PositiveIntegerField()  #lectures per week
    duration_per_lecture = models.PositiveIntegerField()  # duration of lecture
    is_major = models.BooleanField(default=False)  # major or minor ??

    def __str__(self):
        return self.name


class Timeslot(models.Model):
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
        ('Friday', 'Friday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class Department(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=100)  # 1st, 2nd, 3rd, or final year
    teachers = models.ManyToManyField(Teacher)  # dept can have many teachers
    major_subjects = models.ManyToManyField(Subject, related_name='major_in_departments', limit_choices_to={'is_major': True})
    minor_subjects = models.ManyToManyField(Subject, related_name='minor_in_departments', limit_choices_to={'is_major': False})
    total_lectures_per_week = models.PositiveIntegerField()
    start_time = models.TimeField()  #dept starting time
    end_time = models.TimeField()  # dept closing time

    def __str__(self):
        return f"{self.name} - {self.year} Year"


class TimeTable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)  # each subject can have multiple time slots
    year_group = models.CharField(max_length=20, choices=[
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'), # final year 
        ('Final Year', 'Final Year') # or this
    ])

    def __str__(self):
        return f"{self.department.name} - {self.subject.name} ({self.year_group}) - {self.timeslot}"

    class Meta:
        unique_together = ('department', 'subject', 'timeslot', 'year_group')