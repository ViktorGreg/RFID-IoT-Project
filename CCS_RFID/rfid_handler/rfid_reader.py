import serial
import requests
import time
import sys
import re

ARDUINO_PORT = 'COM21'
BAUD_RATE = 9600
DJANGO_URL = 'http://127.0.0.1:8000'

def extract_rfid_from_line(line):
    """Extract RFID UID from Arduino output line"""
    match = re.search(r'Card UID: ([0-9A-F ]+)', line)
    if match:
        return match.group(1).strip()
    return None

def main():
    print("=" * 50)
    print("RFID Reader Starting...")
    print(f"Arduino Port: {ARDUINO_PORT}")
    print("=" * 50)
    
    try:
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("Connected to Arduino. Waiting for cards...\n")
        
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                
                if line:
                    print(f"Arduino: {line}")
                    
                    # Extract RFID from the line
                    rfid_tag = extract_rfid_from_line(line)
                    
                    if rfid_tag:
                        print(f"RFID Detected: {rfid_tag}")
                        
                        # Check for pending registration
                        try:
                            pending_response = requests.get(
                                f'{DJANGO_URL}/api/pending-rfid/check/',
                                timeout=2
                            )
                            
                            if pending_response.status_code == 200:
                                pending = pending_response.json()
                                
                                if pending.get('waiting'):
                                    student_id = pending['student_id']
                                    print(f"Pending registration for student ID: {student_id}")
                                    
                                    # Send to Django
                                    response = requests.post(
                                        f'{DJANGO_URL}/api/rfid/',
                                        json={
                                            'rfid_tag': rfid_tag,
                                            'student_id': student_id
                                        },
                                        timeout=2
                                    )
                                    
                                    if response.status_code == 200:
                                        print("✅ RFID REGISTERED SUCCESSFULLY!")
                                    else:
                                        print(f"❌ Error: {response.json()}")
                                else:
                                    # Normal attendance
                                    response = requests.post(
                                        f'{DJANGO_URL}/api/rfid/',
                                        json={'rfid_tag': rfid_tag},
                                        timeout=2
                                    )
                                    
                                    if response.status_code == 200:
                                        print("✅ Attendance recorded")
                                    else:
                                        print("❌ Unknown card")
                            else:
                                print(f"API error: {pending_response.status_code}")
                                
                        except Exception as e:
                            print(f"Error contacting Django: {e}")
                        
                        print()  # Empty line
            
            time.sleep(0.05)
            
    except serial.SerialException as e:
        print(f"Cannot open {ARDUINO_PORT}: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ser.close()
        sys.exit(0)

if __name__ == "__main__":
    main()