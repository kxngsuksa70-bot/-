"""
SQLite Database Layer (Emergency Local Mode)
ใช้ SQLite แทน Supabase เพื่อให้รันได้ทันทีโดยไม่ต้องเชื่อมต่อ Cloud
"""

import sqlite3
import os
import json
import time

# Database file path
DB_FILE = 'teachmap.db'

def get_connection():
    """สร้าง Connection ไปยัง SQLite"""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # ให้ return เป็น dict-like object
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def init_database():
    """สร้างตารางและข้อมูลตั้งต้น"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # 1. Teachers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                subject TEXT,
                contact TEXT,
                room TEXT,
                profile_picture TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Students Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 3. Schedule Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                day TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT DEFAULT '',
                duration REAL NOT NULL,
                subject TEXT NOT NULL,
                course_code TEXT DEFAULT '',
                classroom TEXT DEFAULT '',
                color TEXT NOT NULL,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        
        # Check if data exists
        cursor.execute("SELECT COUNT(*) FROM teachers")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Creating sample data...")
            # Sample Teachers
            teachers_data = [
                ('teacher1', '1234', 'นางสาวศิริรัตน์ เชื้อแก้ว', 'Computer Science', '089-000-1236', 'Room 927'),
                ('teacher2', '1234', 'Prof. Emily Johnson', 'Chemistry', '089-000-1237', 'Room 202')
            ]
            cursor.executemany("INSERT INTO teachers (username, password, name, subject, contact, room) VALUES (?, ?, ?, ?, ?, ?)", teachers_data)
            
            # Sample Students
            cursor.execute("INSERT INTO students (username, password, name) VALUES ('student1', '1234', 'นักศึกษาทดสอบ')")
            
            # Sample Schedule for Teacher 1
            cursor.execute("SELECT id FROM teachers WHERE username = 'teacher1'")
            t1_id = cursor.fetchone()[0]
            
            schedules_t1 = [
                (t1_id, 'Mon', '08:30', '10:00', 1.5, 'Intro to Prog', 'CS101', '927', '#4285F4'),
                (t1_id, 'Wed', '12:30', '14:30', 2.0, 'Database Sys', 'CS201', '925', '#DB4437'),
                (t1_id, 'Fri', '08:30', '10:00', 1.5, 'Algorithms', 'CS301', '927', '#0F9D58')
            ]
            cursor.executemany("INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", schedules_t1)
            
            # Sample Schedule for Teacher 2
            cursor.execute("SELECT id FROM teachers WHERE username = 'teacher2'")
            t2_id = cursor.fetchone()[0]
            
            schedules_t2 = [
                (t2_id, 'Tue', '08:30', '10:00', 1.5, 'Organic Chem', 'CHEM201', '925', '#F4B400'),
                (t2_id, 'Thu', '13:30', '15:00', 1.5, 'Lab Work', 'CHEM202', '925', '#4285F4')
            ]
            cursor.executemany("INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", schedules_t2)
            
            conn.commit()
            print("Sample data created successfully")
            
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        conn.close()

# ==================== Mock Supabase Client (For Compatibility) ====================
class MockSupabaseClient:
    def __init__(self):
        self.table_name = None
    
    def table(self, name):
        self.table_name = name
        return self

    # This is a very basic mock and might need adjustment based on usage
    def select(self, *args, **kwargs):
        return self
    
    def eq(self, *args, **kwargs):
        return self
    
    def execute(self):
        return MockResponse([])

class MockResponse:
    def __init__(self, data):
        self.data = data

def get_supabase_client():
    """Mock for compatibility"""
    return MockSupabaseClient()

# ==================== Teacher Functions ====================

def get_teacher_by_username(username):
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def verify_teacher(username, password):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        print(f"DEBUG: Checking login for user='{username}' pass='{password}'")
        cursor.execute("SELECT id, password FROM teachers WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            print(f"DEBUG: Found user in DB. DB_pass='{row['password']}'")
            if row['password'] == password:
                print("DEBUG: Password MATCH!")
                return True
            else:
                print("DEBUG: Password MISMATCH!")
                return False
        else:
            print("DEBUG: User NOT FOUND")
            return False
    except Exception as e:
        print(f"DEBUG Error: {e}")
        return False
    finally:
        conn.close()

def get_teacher_schedule(teacher_id):
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, day, start_time, end_time, duration, subject, course_code, classroom, color
            FROM schedule WHERE teacher_id = ?
        """, (teacher_id,))
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            item = dict(row)
            # Map start_time to start for frontend compatibility
            # In database_supabase.py it maps manually
            schedule_item = {
                'id': item['id'],
                'day': item['day'],
                'start': item['start_time'],
                'end': item['end_time'],
                'duration': float(item['duration']) if item['duration'] else 0.0,
                'subject': item['subject'],
                'course_code': item.get('course_code', ''),
                'classroom': item.get('classroom', ''),
                'color': item['color']
            }
            result.append(schedule_item)
        
        # Sort manually
        days = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
        result.sort(key=lambda x: (days.get(x['day'], 8), x['start']))
        
        return result
    finally:
        conn.close()

def update_teacher_profile(teacher_id, username, name, subject, contact, room):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        # Check duplicate username
        if username:
            cursor.execute("SELECT id FROM teachers WHERE username = ? AND id != ?", (username, teacher_id))
            if cursor.fetchone():
                return False
        
        cursor.execute("""
            UPDATE teachers 
            SET username = ?, name = ?, subject = ?, contact = ?, room = ?
            WHERE id = ?
        """, (username, name, subject, contact, room, teacher_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False
    finally:
        conn.close()

# ==================== Schedule Functions ====================

def add_schedule(teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding schedule: {e}")
        return False
    finally:
        conn.close()

def update_schedule(schedule_id, day, start_time, end_time, duration, subject, course_code, classroom, color):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE schedule
            SET day = ?, start_time = ?, end_time = ?, duration = ?, subject = ?, course_code = ?, classroom = ?, color = ?
            WHERE id = ?
        """, (day, start_time, end_time, duration, subject, course_code, classroom, color, schedule_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating schedule: {e}")
        return False
    finally:
        conn.close()

def delete_schedule(schedule_id):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule WHERE id = ?", (schedule_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        return False
    finally:
        conn.close()

# ==================== Student Functions ====================

def verify_student(username, password):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM students WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone() is not None
    finally:
        conn.close()

def get_all_teachers_with_schedule():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, subject, contact, room, profile_picture FROM teachers")
        teachers = [dict(row) for row in cursor.fetchall()]
        
        for teacher in teachers:
            teacher['schedule'] = get_teacher_schedule(teacher['id'])
            teacher['time'] = teacher.get('contact', '')
            
            classrooms = set()
            for item in teacher['schedule']:
                if item.get('classroom'):
                    classrooms.add(item['classroom'])
            teacher['classrooms'] = ', '.join(sorted(classrooms)) if classrooms else '-'
            
        return teachers
    finally:
        conn.close()

def get_all_teacher_schedules():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, t.name as teacher_name, t.room as teacher_room
            FROM schedule s
            JOIN teachers t ON s.teacher_id = t.id
        """)
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            item = dict(row)
            schedule_item = {
                'day': item['day'],
                'start': item['start_time'],
                'end': item['end_time'],
                'duration': float(item['duration']) if item['duration'] else 0.0,
                'subject': item['subject'],
                'course_code': item.get('course_code', ''),
                'classroom': item.get('classroom', ''),
                'color': item['color'],
                'teacher_name': item['teacher_name'],
                'teacher_room': item['teacher_room']
            }
            result.append(schedule_item)
            
        days = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
        result.sort(key=lambda x: (days.get(x['day'], 8), x['start']))
        
        return result
    finally:
        conn.close()

# ==================== User Management Functions ====================

def get_all_teachers():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, name, subject, contact, room, created_at FROM teachers")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def get_all_students():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, name, created_at FROM students")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def add_teacher(username, password, name, subject, contact, room):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO teachers (username, password, name, subject, contact, room)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password, name, subject, contact, room))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding teacher: {e}")
        return False
    finally:
        conn.close()

def add_student(username, password, name):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (username, password, name) VALUES (?, ?, ?)", (username, password, name))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding student: {e}")
        return False
    finally:
        conn.close()

def delete_teacher(teacher_id):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting teacher: {e}")
        return False
    finally:
        conn.close()

def delete_student(student_id):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting student: {e}")
        return False
    finally:
        conn.close()

# ==================== Helper Functions ====================

def get_teacher_by_id(teacher_id):
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE id = ?", (teacher_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_student_by_id(student_id):
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_student_by_username(username):
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
