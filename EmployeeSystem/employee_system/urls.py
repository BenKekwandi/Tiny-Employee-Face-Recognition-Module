from django.contrib import admin
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('login', views.login),
    path('home',views.home),
    path('create-employee',views.create_employee),
    path('recognition',views.recognize_employee),
    path('employee-list',views.list_employee),
    path('test',views.recognition_test)
]
