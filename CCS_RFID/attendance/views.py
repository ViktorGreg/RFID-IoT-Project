from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def attendance(request):
    return render(request, 'attendance.html')

@login_required
def student_attendance(request):
    """Student attendance record page"""
    from classes.models import Enrollment, Attendance, ClassSession
    from django.db.models import Count, Q
    
    # Get all enrollments for this student
    enrollments = Enrollment.objects.filter(student=request.user).select_related('class_obj')
    
    subjects = []
    total_present = 0
    total_absent = 0
    total_late = 0
    total_classes_attended = 0
    
    for enrollment in enrollments:
        class_obj = enrollment.class_obj
        
        # Get all sessions for this class
        sessions = ClassSession.objects.filter(class_obj=class_obj)
        
        # Get attendance records for this student in this class
        attendances = Attendance.objects.filter(
            student=request.user,
            session__class_obj=class_obj
        )
        
        present_count = attendances.filter(status='present').count()
        late_count = attendances.filter(status='late').count()
        absent_count = attendances.filter(status='absent').count()
        
        total_present += present_count
        total_late += late_count
        total_absent += absent_count
        
        total_sessions = sessions.count()
        attended = present_count + late_count
        total_classes_attended += attended
        
        attendance_percentage = int((attended / total_sessions) * 100) if total_sessions > 0 else 0
        
        subjects.append({
            'id': class_obj.id,
            'name': class_obj.subject_description,
            'code': class_obj.subject_code,
            'schedule_day': class_obj.day,
            'time_start': class_obj.time_from,
            'time_end': class_obj.time_to,
            'present_count': present_count,
            'late_count': late_count,
            'absence_count': absent_count,
            'total_classes': total_sessions,
            'attendance_percentage': attendance_percentage,
            'absences_left': 5 - absent_count if absent_count < 5 else 0,
        })
    
    # Calculate overall attendance percentage
    total_records = total_present + total_late + total_absent
    overall_attendance = int(((total_present + total_late) / total_records) * 100) if total_records > 0 else 0
    
    # Get recent attendance records (last 10)
    recent_attendance = Attendance.objects.filter(
        student=request.user
    ).select_related('session__class_obj').order_by('-time_in')[:10]
    
    recent_data = []
    for att in recent_attendance:
        recent_data.append({
            'date': att.time_in,
            'time_in': att.time_in,
            'status': att.status,
            'subject_name': att.session.class_obj.subject_description if att.session else 'N/A',
            'subject_code': att.session.class_obj.subject_code if att.session else 'N/A',
        })
    
    context = {
        'subjects': subjects,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_late': total_late,
        'overall_attendance': overall_attendance,
        'recent_attendance': recent_data,
    }
    
    return render(request, 'student_attendance.html', context)