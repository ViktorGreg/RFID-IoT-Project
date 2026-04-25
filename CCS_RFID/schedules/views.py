from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from classes.models import Class

@login_required
def schedule(request):
    """Display the class schedule page"""
    return render(request, 'schedule.html')

@login_required
def teacher_schedule(request):
    """API endpoint to get teacher's class schedule"""
    try:
        # Get all classes for the logged-in teacher
        classes = Class.objects.filter(teacher=request.user)
        
        print(f"[DEBUG] Found {classes.count()} classes for teacher {request.user.email}")
        
        schedule_list = []
        for class_obj in classes:
            # Extract the actual day from the day field
            # The day field contains values like "W (Lec 0.00) (Lab 1.00)" or "T (Lec 2.00) (Lab 0.00)"
            day_raw = class_obj.day or ''
            day_cleaned = extract_day_from_raw(day_raw)
            
            print(f"[DEBUG] Class {class_obj.subject_code}: raw day = '{day_raw}', cleaned day = '{day_cleaned}'")
            
            schedule_list.append({
                'id': class_obj.id,
                'subject_code': class_obj.subject_code,
                'subject_description': class_obj.subject_description,
                'day': day_cleaned,  # Send the cleaned day
                'time_from': class_obj.time_from.strftime('%H:%M') if class_obj.time_from else '06:00',
                'time_to': class_obj.time_to.strftime('%H:%M') if class_obj.time_to else '19:00',
                'room': class_obj.room or 'TBA',
                'section': class_obj.section or '',
                'college': class_obj.college or '',
                'semester': class_obj.semester or '',
                'school_year': class_obj.school_year or ''
            })
        
        print(f"[DEBUG] Sending {len(schedule_list)} classes")
        return JsonResponse(schedule_list, safe=False)
    except Exception as e:
        print(f"[ERROR] teacher_schedule: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def extract_day_from_raw(day_raw):
    """Extract the actual day from raw day string"""
    if not day_raw:
        return ''
    
    day_raw = day_raw.strip().upper()
    
    # Map of abbreviations to full day names
    day_map = {
        'M': 'monday',
        'MON': 'monday',
        'MONDAY': 'monday',
        'T': 'tuesday',
        'TUE': 'tuesday',
        'TUESDAY': 'tuesday',
        'W': 'wednesday',
        'WED': 'wednesday',
        'WEDNESDAY': 'wednesday',
        'TH': 'thursday',
        'THU': 'thursday',
        'THURSDAY': 'thursday',
        'F': 'friday',
        'FRI': 'friday',
        'FRIDAY': 'friday',
        'S': 'saturday',
        'SAT': 'saturday',
        'SATURDAY': 'saturday',
        'SUN': 'sunday',
        'SUNDAY': 'sunday'
    }
    
    # Check if the raw day starts with any of the abbreviations
    for abbr, full_day in day_map.items():
        if day_raw.startswith(abbr):
            return full_day
    
    return 'monday'  # Default fallback