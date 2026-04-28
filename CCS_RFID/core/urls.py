from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activity/', views.activity, name='activity'),
    path('stud_dashboard/', views.stud_dashboard, name='stud_dashboard'),
    path('student_subject/', views.student_subject, name='student_subject'),
    path('student_view_class/', views.student_view_class, name='student_view_class'),
    
    # Superadmin URLs
    path('super-dashboard/', views.super_dashboard, name='super_dashboard'),
    path('super-activity/', views.super_activity, name='super_activity'),  # ADD THIS LINE
    path('user-management/', views.user_management, name='user_management'),
    path('edit-student/<int:user_id>/', views.edit_student, name='edit_student'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # API URLs
    path('api/activity-log/', views.get_activity_log, name='get_activity_log'),
    path('api/super-activity-log/', views.get_super_activity_log, name='super_activity_log'),  # ADD THIS LINE
    path('api/update-attendance-status/', views.update_attendance_status, name='update_attendance_status'),
    path('profile/', views.profile, name='profile'),
]