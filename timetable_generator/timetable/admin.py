from django.contrib import admin
from .models import Professor, Subject, TimeSlot

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__username', 'specialization')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'professor')
    search_fields = ('name', 'department', 'professor__user__username')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time')
    search_fields = ('day',)
