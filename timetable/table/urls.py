from django.urls import path 
from . views import * 

urlpatterns = [
    path ('', home , name = 'home'),
    path ('register/' , register, name='register'),
    path('login/' , login_view , name= 'login'),
    path('logout/' , logout_view , name = 'logout'),
    path('profile/' , profile , name = 'profile'),
    path('data/', data, name = 'data'),
    path('generate/' , generate, name = 'generate'),
]