"""
Supabase REST API Database Layer
ใช้ Supabase Python Client แทนการเชื่อมต่อ PostgreSQL โดยตรง
เพื่อแก้ปัญหา IPv6 บน Railway
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

# Initialize Supabase client
supabase: Client = None

def init_supabase():
    """Initialize Supabase client"""
    global supabase
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing Supabase client: {e}")
        return False

def get_supabase_client():
    """Get Supabase client instance"""
    global supabase
    if supabase is None:
        init_supabase()
    return supabase

# ==================== Teacher Functions ====================

def get_teacher_by_username(username):
    """ดึงข้อมูลอาจารย์จาก username"""
    try:
        client = get_supabase_client()
        response = client.table('teachers').select('*').eq('username', username).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching teacher: {e}")
        return None

def verify_teacher(username, password):
    """ตรวจสอบข้อมูลอาจารย์"""
    try:
        client = get_supabase_client()
        response = client.table('teachers').select('id').eq('username', username).eq('password', password).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error verifying teacher: {e}")
        return False

def get_teacher_schedule(teacher_id):
    """ดึงตารางสอนของอาจารย์"""
    try:
        client = get_supabase_client()
        response = client.table('schedule').select('id, day, start_time, end_time, duration, subject, course_code, classroom, color').eq('teacher_id', teacher_id).execute()
        
        # Convert to expected format
        result = []
        for item in response.data:
            schedule_item = {
                'id': item['id'],
                'day': item['day'],
                'start': item['start_time'],
                'end': item['end_time'],
                'duration': float(item['duration']) if item.get('duration') else 0.0,
                'subject': item['subject'],
                'course_code': item.get('course_code', ''),
                'classroom': item.get('classroom', ''),
                'color': item['color']
            }
            result.append(schedule_item)
        
        return result
    except Exception as e:
        print(f"Error fetching schedule: {e}")
        return []

def update_teacher_profile(teacher_id, username, name, subject, contact, room):
    """อัปเดตข้อมูลโปรไฟล์อาจารย์"""
    try:
        client = get_supabase_client()
        
        # Check if username already exists
        if username:
            existing = client.table('teachers').select('id').eq('username', username).neq('id', teacher_id).execute()
            if existing.data:
                return False  # Username already taken
        
        # Update profile
        client.table('teachers').update({
            'username': username,
            'name': name,
            'subject': subject,
            'contact': contact,
            'room': room
        }).eq('id', teacher_id).execute()
        
        return True
    except Exception as e:
        print(f"Error updating teacher profile: {e}")
        return False

# ==================== Schedule Functions ====================

def add_schedule(teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color):
    """เพิ่มคาบสอนใหม่"""
    try:
        client = get_supabase_client()
        client.table('schedule').insert({
            'teacher_id': teacher_id,
            'day': day,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'subject': subject,
            'course_code': course_code,
            'classroom': classroom,
            'color': color
        }).execute()
        return True
    except Exception as e:
        print(f"Error adding schedule: {e}")
        return False

def update_schedule(schedule_id, day, start_time, end_time, duration, subject, course_code, classroom, color):
    """อัพเดทคาบสอน"""
    try:
        client = get_supabase_client()
        client.table('schedule').update({
            'day': day,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'subject': subject,
            'course_code': course_code,
            'classroom': classroom,
            'color': color
        }).eq('id', schedule_id).execute()
        return True
    except Exception as e:
        print(f"Error updating schedule: {e}")
        return False

def delete_schedule(schedule_id):
    """ลบคาบสอน"""
    try:
        client = get_supabase_client()
        client.table('schedule').delete().eq('id', schedule_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        return False

# ==================== Student Functions ====================

def verify_student(username, password):
    """ตรวจสอบข้อมูลนักศึกษา"""
    try:
        client = get_supabase_client()
        response = client.table('students').select('id').eq('username', username).eq('password', password).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error verifying student: {e}")
        return False

def get_all_teachers_with_schedule():
    """ดึงข้อมูลอาจารย์ทั้งหมดพร้อมตารางสอน"""
    try:
        client = get_supabase_client()
        response = client.table('teachers').select('id, name, subject, contact, room, profile_picture').execute()
        
        result = []
        for teacher in response.data:
            teacher_dict = dict(teacher)
            teacher_dict['schedule'] = get_teacher_schedule(teacher_dict['id'])
            teacher_dict['time'] = teacher_dict.get('contact', '')
            
            # รวมห้องเรียนจากตารางสอน
            classrooms = set()
            for schedule_item in teacher_dict['schedule']:
                if schedule_item.get('classroom'):
                    classrooms.add(schedule_item['classroom'])
            
            teacher_dict['classrooms'] = ', '.join(sorted(classrooms)) if classrooms else '-'
            result.append(teacher_dict)
        
        return result
    except Exception as e:
        print(f"Error fetching all teachers: {e}")
        return []

def get_all_teacher_schedules():
    """ดึงตารางสอนทั้งหมด (สำหรับนักศึกษา)"""
    try:
        client = get_supabase_client()
        # Get schedules with teacher info
        response = client.table('schedule').select(
            'day, start_time, end_time, duration, subject, course_code, classroom, color, teachers(name, room)'
        ).execute()
        
        result = []
        for item in response.data:
            schedule_item = {
                'day': item['day'],
                'start': item['start_time'],
                'end': item['end_time'],
                'duration': float(item.get('duration', 0)),
                'subject': item['subject'],
                'course_code': item.get('course_code', ''),
                'classroom': item.get('classroom', ''),
                'color': item['color'],
                'teacher_name': item['teachers']['name'] if item.get('teachers') else '',
                'teacher_room': item['teachers']['room'] if item.get('teachers') else ''
            }
            result.append(schedule_item)
        
        return result
    except Exception as e:
        print(f"Error fetching all schedules: {e}")
        return []

# ==================== User Management Functions ====================

def get_all_teachers():
    """ดึงรายการอาจารย์ทั้งหมด"""
    try:
        client = get_supabase_client()
        response = client.table('teachers').select('id, username, name, subject, contact, room, created_at').execute()
        return response.data
    except Exception as e:
        print(f"Error fetching teachers: {e}")
        return []

def get_all_students():
    """ดึงรายการนักศึกษาทั้งหมด"""
    try:
        client = get_supabase_client()
        response = client.table('students').select('id, username, name, created_at').execute()
        return response.data
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []

def add_teacher(username, password, name, subject, contact, room):
    """เพิ่มอาจารย์ใหม่"""
    try:
        client = get_supabase_client()
        client.table('teachers').insert({
            'username': username,
            'password': password,
            'name': name,
            'subject': subject,
            'contact': contact,
            'room': room
        }).execute()
        return True
    except Exception as e:
        print(f"Error adding teacher: {e}")
        return False

def add_student(username, password, name):
    """เพิ่มนักศึกษาใหม่"""
    try:
        client = get_supabase_client()
        client.table('students').insert({
            'username': username,
            'password': password,
            'name': name
        }).execute()
        return True
    except Exception as e:
        print(f"Error adding student: {e}")
        return False

def delete_teacher(teacher_id):
    """ลบอาจารย์"""
    try:
        client = get_supabase_client()
        client.table('teachers').delete().eq('id', teacher_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting teacher: {e}")
        return False

def delete_student(student_id):
    """ลบนักศึกษา"""
    try:
        client = get_supabase_client()
        client.table('students').delete().eq('id', student_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting student: {e}")
        return False

# Helper functions for compatibility
def get_teacher_by_id(teacher_id):
    """Get teacher by ID"""
    try:
        client = get_supabase_client()
        response = client.table('teachers').select('*').eq('id', teacher_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching teacher by ID: {e}")
        return None

def get_student_by_id(student_id):
    """Get student by ID"""
    try:
        client = get_supabase_client()
        response = client.table('students').select('*').eq('id', student_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching student by ID: {e}")
        return None

def get_student_by_username(username):
    """Get student by username"""
    try:
        client = get_supabase_client()
        response = client.table('students').select('*').eq('username', username).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching student by username: {e}")
        return None

def init_database():
    """Initialize database (compatibility function)"""
    return init_supabase()
