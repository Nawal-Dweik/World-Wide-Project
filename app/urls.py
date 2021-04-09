from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('login_page', views.login_page),
    path('registration', views.registration_page),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),

    #############################################

    path('groups', views.groupDashboard),
    path('groups/add', views.addGroup),
    path('join/<int:group_id>', views.joinGroup),
    path('groups/destination/<int:group_id>', views.view_destination),
   
]
