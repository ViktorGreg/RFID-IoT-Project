from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def activity(request):
    return render(request, 'activity.html')

@login_required
def stud_dashboard(request):
    return render(request, 'stud_dashboard.html')

@login_required
def student_subject(request):
    return render(request, 'student_subject.html')