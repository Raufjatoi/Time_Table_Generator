from django.db import models

TIME_SLOTS = [
    ('8:30 - 9:30', '8:30 - 9:30'),
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('11:00 - 12:00', '11:00 - 12:00'),
    ('12:00 - 1:00', '12:00 - 1:00'),
    ('1:00 - 2:00', '1:00 - 2:00'),
    ('2:00 - 3:00', '2:00 - 3:00'),
    ('3:00 - 4:00', '3:00 - 4:00'),
    ('4:00 - 5:00', '4:00 - 5:00'),
]

DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]

YEAR_GROUPS = [
    ('1st Year', '1st Year'),
    ('2nd Year', '2nd Year'),
    ('3rd Year', '3rd Year'),
    ('4th Year', '4th Year'),
    ('Final Year', 'Final Year'),
]

SEMESTERS = [
    ('1st Semester', '1st Semester'),
    ('2nd Semester', '2nd Semester'),
    ('3rd Semester', '3rd Semester'),
    ('4th Semester', '4th Semester'),
    ('5th Semester', '5th Semester'),
    ('6th Semester', '6th Semester'),
    ('7th Semester', '7th Semester'),
    ('8th Semester', '8th Semester'),
]

class Timeslot(models.Model):
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.CharField(max_length=20, choices=TIME_SLOTS, default='8:30 - 9:30')
    end_time = models.CharField(max_length=20, choices=TIME_SLOTS, default='1:00 - 2:00')

    def __str__(self):
        return f"{self.day} - {self.start_time}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    lectures_per_week = models.PositiveIntegerField()
    duration_per_lecture = models.PositiveIntegerField()
    is_major = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    working_hours = models.CharField(max_length=20, choices=TIME_SLOTS)
    available_time_slots = models.ManyToManyField(Timeslot, related_name='available_teachers')
    subjects = models.ManyToManyField(Subject, related_name='assigned_teachers')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=20, choices=YEAR_GROUPS)
    semester = models.CharField(max_length=20, choices=SEMESTERS)
    teachers = models.ManyToManyField(Teacher)
    major_subjects = models.ManyToManyField(Subject, related_name='major_in_departments', limit_choices_to={'is_major': True})
    minor_subjects = models.ManyToManyField(Subject, related_name='minor_in_departments', limit_choices_to={'is_major': False})
    total_lectures_per_week = models.PositiveIntegerField()
    start_time = models.CharField(max_length=20, choices=TIME_SLOTS, default='8:30 - 9:30')
    end_time = models.CharField(max_length=20, choices=TIME_SLOTS, default='1:00 - 2:00')

    def __str__(self):
        return f"{self.name} - {self.year} ({self.semester})"

class TimeTable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    year_group = models.CharField(max_length=20, choices=YEAR_GROUPS)
    semester = models.CharField(max_length=20, choices=SEMESTERS)

    def __str__(self):
        return f"{self.department.name} - {self.subject.name} ({self.year_group}, {self.semester}) - {self.timeslot}"

    class Meta:
        unique_together = ('department', 'subject', 'timeslot', 'year_group', 'semester')
