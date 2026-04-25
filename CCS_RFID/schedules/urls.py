from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule, name='schedule'),
    path('api/teacher-schedule/', views.teacher_schedule, name='teacher_schedule'),
]