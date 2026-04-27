from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from classes.models import Enrollment, Class, ClassSession, Attendance
import json


@login_required
def dashboard(request):
    """Teacher dashboard"""
    return render(request, 'dashboard.html')


@login_required
def activity(request):
    """Activity log page"""
    return render(request, 'activity.html')


@login_required
def stud_dashboard(request):
    """Student dashboard"""
    return render(request, 'stud_dashboard.html')


@login_required
def student_subject(request):
    """Display all subjects the student is enrolled in"""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('class_obj')
    
    subjects = []
    unique_days = set()
    
    for enrollment in enrollments:
        class_obj = enrollment.class_obj
        subjects.append({
            'id': class_obj.id,
            'name': class_obj.subject_description,
            'code': class_obj.subject_code,
            'description': class_obj.subject_description,
            'schedule_day': class_obj.day,
            'time_start': class_obj.time_from,
            'time_end': class_obj.time_to,
            'room': class_obj.room,
            'units': class_obj.class_size or 3,
            'status': enrollment.status,
            'absences': enrollment.absence_count,
        })
        unique_days.add(class_obj.day)
    
    # Create time slots from 7 AM to 8 PM
    time_slots = []
    for hour in range(7, 20):
        am_pm = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        next_hour = hour + 1
        next_display_hour = next_hour if next_hour <= 12 else next_hour - 12
        next_am_pm = "AM" if next_hour < 12 else "PM"
        
        time_slots.append({
            'label': f"{display_hour}:00 {am_pm} - {next_display_hour}:00 {next_am_pm}",
            'hour': f"{hour:02d}"
        })
    
    context = {
        'subjects': subjects,
        'total_units': sum(s['units'] for s in subjects),
        'days_per_week': len(unique_days),
        'time_slots': time_slots,
        'current_semester': '2024-2025',
    }
    return render(request, 'student_subject.html', context)


@login_required
def student_view_class(request):
    """Display class details for a student (view only)"""
    class_id = request.GET.get('class_id')
    if not class_id:
        return redirect('student_subject')
    
    class_obj = get_object_or_404(Class, id=class_id)
    
    # Get all enrollments for this class
    enrollments = Enrollment.objects.filter(class_obj=class_obj).select_related('student')
    
    # Get the current student's enrollment
    user_enrollment = enrollments.filter(student=request.user).first()
    
    students = []
    for enrollment in enrollments:
        student = enrollment.student
        students.append({
            'name': student.get_full_name(),
            'student_id': student.student_id if hasattr(student, 'student_id') else '',
            'email': student.email,
            'gender': getattr(student, 'gender', 'N/A'),
            'status': enrollment.status,
            'absences': enrollment.absence_count,
        })
    
    context = {
        'class': class_obj,
        'students': students,
        'total_students': len(students),
        'user_status': user_enrollment.status if user_enrollment else 'not_enrolled',
        'user_absences': user_enrollment.absence_count if user_enrollment else 0,
        'user_absences_left': 5 - (user_enrollment.absence_count if user_enrollment else 0),
    }
    return render(request, 'student_view_class.html', context)


@login_required
def get_activity_log(request):
    """API endpoint to get activity log - FIXED VERSION"""
    try:
        # Get ALL attendance records
        attendances = Attendance.objects.all().select_related('student', 'session__class_obj').order_by('-time_in')
        
        activities = []
        
        for attendance in attendances:
            student = attendance.student
            session = attendance.session
            class_obj = session.class_obj if session else None
            
            activities.append({
                'id': attendance.id,
                'student_name': student.get_full_name(),
                'student_id': student.student_id if hasattr(student, 'student_id') else 'N/A',
                'class_name': class_obj.subject_code if class_obj else 'N/A',
                'class_description': class_obj.subject_description if class_obj else 'N/A',
                'section': class_obj.section if class_obj and class_obj.section else 'N/A',
                'date': session.start_time.strftime('%B %d, %Y') if session else 'N/A',
                'time': attendance.time_in.strftime('%I:%M %p') if attendance.time_in else 'N/A',
                'status': attendance.status
            })
        
        return JsonResponse({
            'success': True,
            'activities': activities
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def update_attendance_status(request):
    """API endpoint to update attendance status"""
    try:
        data = json.loads(request.body)
        attendance_id = data.get('attendance_id')
        new_status = data.get('status')
        
        attendance = Attendance.objects.get(id=attendance_id)
        
        # Verify valid status
        valid_statuses = ['present', 'late', 'absent']
        if new_status not in valid_statuses:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
        
        # Update status
        attendance.status = new_status
        attendance.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Status updated to {new_status}'
        })
        
    except Attendance.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Attendance record not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)