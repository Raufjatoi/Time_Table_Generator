from django.db import models

# teacher model that stores teacher details
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.TextField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# subject group model that stores subject group details like the 1st year, 2nd year, etc.
class SubjectGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# subject model that stores subject details
class Subject(models.Model):
    MAJOR = 'Major'
    MINOR = 'Minor'
    SUBJECT_TYPES = [
        (MAJOR, 'Major'),
        (MINOR, 'Minor'),
    ]

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=SUBJECT_TYPES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

# this model is used to map the subjects to the subject groups
class SubjectGroupMapping(models.Model):
    group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='groups')

    class Meta:
        unique_together = ('group', 'subject')

# department model that stores department details like the department name, short name, year, major subjects, and minor subjects
class Department(models.Model):
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    year = models.IntegerField()
    major_subjects = models.ForeignKey(
        SubjectGroup, on_delete=models.SET_NULL, null=True, related_name='major_departments'
    )
    minor_subjects = models.ForeignKey(
        SubjectGroup, on_delete=models.SET_NULL, null=True, related_name='minor_departments'
    )

    def __str__(self):
        return f"{self.full_name} ({self.short_name})"

class Day(models.Model):
    day_name = models.CharField(max_length=20)

    def __str__(self):
        return self.day_name


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Break(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='breaks')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='breaks')

    def __str__(self):
        return f"{self.day.day_name}: {self.start_time} - {self.end_time}"

# this will generate like the time table hope so it will be useful for us
class Schedule(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='schedules')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules')
    room_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = [
            ('day', 'time_slot', 'teacher'),
            ('day', 'time_slot', 'department'),
        ]

    def __str__(self):
        return f"{self.day.day_name}, {self.time_slot}: {self.subject.name}"