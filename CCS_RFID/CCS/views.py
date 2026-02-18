from django.shortcuts import render

def login(request):
    return render(request, 'login.html', {})

def dashboard(request):
    return render(request, 'dashboard.html')

def attendance(request):
    return render(request, 'attendance.html')  # Create this template

def classes(request):
    return render(request, 'classes.html')  # Create this template

def activity(request):
    return render(request, 'activity.html')  # Create this template

def schedule(request):
    return render(request, 'schedule.html')  # Create this template