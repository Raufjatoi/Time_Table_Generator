from django.contrib import admin
from .models import Teacher, Subject, Department, Timeslot, TimeTable

admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(Timeslot)
admin.site.register(TimeTable)
