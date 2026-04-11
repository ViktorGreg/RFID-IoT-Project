from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def attendance(request):
    return render(request, 'attendance.html')

@login_required
def student_attendance(request):
    return render(request, 'student_attendance.html')