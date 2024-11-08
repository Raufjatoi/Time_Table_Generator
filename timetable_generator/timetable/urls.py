from django.urls import path
from .views import register, timetable_home, add_professor, add_subject, add_time_slot
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    register,
    timetable_home,
    add_professor,
    add_subject,
    add_time_slot,
    profile_view, 
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('', timetable_home, name='timetable-home'),
    path('add-professor/', add_professor, name='add-professor'),
    path('add-subject/', add_subject, name='add-subject'),
    path('add-time-slot/', add_time_slot, name='add-time-slot'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='timetable/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='timetable/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('accounts/profile/', profile_view, name='profile'), 
]