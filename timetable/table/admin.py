from django.contrib import admin

from .models import Teacher, Subject, SubjectGroup, SubjectGroupMapping, Department, Day

admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(SubjectGroup)
admin.site.register(SubjectGroupMapping)
admin.site.register(Department)
admin.site.register(Day)
