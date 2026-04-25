from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminLogin, name='adminLogin'),
    path('studentLogin/', views.studentLogin, name='studentLogin'),
    path('adminRegistration/', views.adminRegistration, name='adminRegistration'),
    path('studentRegistration/', views.studentRegistration, name='studentRegistration'),
    path('logout/', views.logout_view, name='logout'),
    path('api/rfid/', views.rfid_handler, name='rfid_handler'),  # This line MUST be here
    path('api/check-rfid/<int:student_id>/', views.check_rfid_status, name='check_rfid'),

    path('api/pending-rfid/create/<int:student_id>/', views.create_pending_rfid, name='create_pending_rfid'),
    path('api/pending-rfid/check/', views.check_pending_rfid, name='check_pending_rfid'),
    path('student-registration/', views.studentRegistration, name='studentRegistration'),

    # path('api/update-existing-student/', views.update_existing_student, name='update_existing_student'),
    path('api/receive-rfid/', views.receive_rfid, name='receive_rfid'),
    path('api/get-latest-rfid/', views.get_latest_rfid, name='get_latest_rfid'),
    path('api/claim-existing-account/', views.claim_existing_account, name='claim_existing_account'),
    path('api/check-user-by-rfid/', views.check_user_by_rfid, name='check_user_by_rfid'),
]