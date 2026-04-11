from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.attendance, name='attendance'),
    path('student_attendance/', views.student_attendance, name='student_attendance'),
]