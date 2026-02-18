from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance, name='attendance'),
    path('classes/', views.classes, name='classes'),
    path('activity/', views.activity, name='activity'),
    path('schedule/', views.schedule, name='schedule'),
]
