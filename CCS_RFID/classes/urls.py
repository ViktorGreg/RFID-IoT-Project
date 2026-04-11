from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.classes, name='classes'),
    path('view_class/', views.view_class, name='view_class'),
]