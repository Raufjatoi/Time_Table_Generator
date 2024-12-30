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
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
