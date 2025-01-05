from django.urls import path 
from . views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path ('', home , name = 'home'),
    path ('register/' , register, name='register'),
    path('login/' , login_view , name= 'login'),
    path('logout/' , logout_view , name = 'logout'),
    path('profile/' , profile , name = 'profile'),
    path('data/', data_entry, name='data_entry'),
    path('generate/', generate_timetable, name='generate_timetable'),
    path('add_teacher', add_teacher, name='add_teacher'),
    path('change_pas/', change_password, name='change_pas'),
    path('doc/', doc, name='doc'),
    path('works/', works, name='works'),
    path('us/', us, name='us'),
    path('add_subject', add_subject, name='add_subject'),
    path('add_department', add_department, name='add_department'),
    path('add_timeslot', add_timeslot, name='add_timeslot'),
    
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
