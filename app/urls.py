from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_page),
    path('registration', views.registration_page),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
   
]
