from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def classes(request):
    return render(request, 'classes.html')

@login_required
def view_class(request):
    return render(request, 'view_class.html')