import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
import os
from dotenv import load_dotenv
import socket

# Load environment variables
load_dotenv()

# Resolve hostname to IPv4 address to avoid IPv6 issues on Railway
def get_ipv4_address(hostname):
    """Resolve hostname to IPv4 address only"""
    try:
        # Force IPv4 resolution
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
        if addr_info:
            return addr_info[0][4][0]  # Return first IPv4 address
    except Exception as e:
        print(f"Warning: Could not resolve {hostname} to IPv4, using hostname: {e}")
    return hostname

# Get Supabase host and resolve to IPv4
supabase_host = os.environ.get('SUPABASE_HOST', 'localhost')
resolved_host = get_ipv4_address(supabase_host) if supabase_host != 'localhost' else 'localhost'

# Database configuration from environment variables
DB_CONFIG = {
    'host': resolved_host,
    'port': os.environ.get('SUPABASE_PORT', '5432'),
    'database': os.environ.get('SUPABASE_DB', 'postgres'),
    'user': os.environ.get('SUPABASE_USER', 'postgres'),
    'password': os.environ.get('SUPABASE_PASSWORD', ''),
    'connect_timeout': 10,  # Add timeout to avoid hanging
}

# Connection pool for better performance
connection_pool = None

def init_connection_pool():
    """Initialize PostgreSQL connection pool"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            **DB_CONFIG
        )
        print("✅ PostgreSQL connection pool initialized")
        return True
    except Exception as e:
        print(f"❌ Error creating connection pool: {e}")
        return False

def get_connection():
    """Get a connection from the pool"""
    global connection_pool
    
    # Initialize pool if not exists
    if connection_pool is None:
        if not init_connection_pool():
            return None
    
    try:
        connection = connection_pool.getconn()
        return connection
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        return None

def return_connection(conn):
    """Return connection to the pool"""
    if connection_pool and conn:
        connection_pool.putconn(conn)

def init_database():
    """Create tables if they don't exist"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # สร้างตาราง teachers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                subject VARCHAR(255),
                contact VARCHAR(50),
                room VARCHAR(50),
                profile_picture VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # สร้างตาราง students
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # สร้างตาราง schedule
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id SERIAL PRIMARY KEY,
                teacher_id INTEGER NOT NULL,
                day VARCHAR(10) NOT NULL,
                start_time VARCHAR(10) NOT NULL,
                end_time VARCHAR(10) DEFAULT '',
                duration DECIMAL(3,1) NOT NULL,
                subject VARCHAR(255) NOT NULL,
                course_code VARCHAR(50) DEFAULT '',
                classroom VARCHAR(50) DEFAULT '',
                color VARCHAR(20) NOT NULL,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        
        # ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่
        cursor.execute("SELECT COUNT(*) FROM teachers")
        teacher_count = cursor.fetchone()[0]
        
        if teacher_count == 0:
            # เพิ่มข้อมูลตัวอย่าง (ใช้ bcrypt hash แทน plain text)
            # TODO: Update to use bcrypt hashing
            cursor.execute("""
                INSERT INTO teachers (username, password, name, subject, contact, room)
                VALUES 
                    ('teacher1', '1234', 'นางสาวศิริรัตน์ เชื้อแก้ว', 'Computer Science', '089-000-1236', 'Room 927'),
                    ('teacher2', '1234', 'Prof. Emily Johnson', 'Chemistry', '089-000-1237', 'Room 202')
            """)
            
            cursor.execute("""
                INSERT INTO students (username, password, name) 
                VALUES ('student1', '1234', 'นักศึกษาทดสอบ')
            """)
            
            # Get teacher IDs and add schedules
            cursor.execute("SELECT id FROM teachers WHERE username = 'teacher1'")
            t1 = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color)
                VALUES 
                    (%s, 'Mon', '08:30', '10:00', 1.5, 'Intro to Prog', 'CS101', '927', '#4285F4'),
                    (%s, 'Wed', '12:30', '14:30', 2.0, 'Database Sys', 'CS201', '925', '#DB4437'),
                    (%s, 'Fri', '08:30', '10:00', 1.5, 'Algorithms', 'CS301', '927', '#0F9D58')
            """, (t1, t1, t1))
            
            cursor.execute("SELECT id FROM teachers WHERE username = 'teacher2'")
            t2 = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color)
                VALUES 
                    (%s, 'Tue', '08:30', '10:00', 1.5, 'Organic Chem', 'CHEM201', '925', '#F4B400'),
                    (%s, 'Thu', '13:30', '15:00', 1.5, 'Lab Work', 'CHEM202', '925', '#4285F4')
            """, (t2, t2))
            
            conn.commit()
            print("✅ Sample data created")
        
        cursor.close()
        return_connection(conn)
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

# ==================== Teacher Functions ====================

def get_teacher_by_username(username):
    """ดึงข้อมูลอาจารย์จาก username"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, username, password, name, subject, contact, room, profile_picture
            FROM teachers WHERE username = %s
        """, (username,))
        
        teacher = cursor.fetchone()
        cursor.close()
        return_connection(conn)
        
        return dict(teacher) if teacher else None
        
    except Exception as e:
        print(f"Error fetching teacher: {e}")
        return_connection(conn)
        return None

def verify_teacher(username, password):
    """ตรวจสอบข้อมูลอาจารย์"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM teachers
            WHERE username = %s AND password = %s
        """, (username, password))
        
        result = cursor.fetchone()
        cursor.close()
        return_connection(conn)
        
        return result is not None
        
    except Exception as e:
        print(f"Error verifying teacher: {e}")
        return_connection(conn)
        return False

def get_teacher_schedule(teacher_id):
    """ดึงตารางสอนของอาจารย์"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, day, start_time as start, end_time as end, duration, subject, course_code, classroom, color
            FROM schedule WHERE teacher_id = %s
            ORDER BY 
                CASE day 
                    WHEN 'Mon' THEN 1
                    WHEN 'Tue' THEN 2
                    WHEN 'Wed' THEN 3
                    WHEN 'Thu' THEN 4
                    WHEN 'Fri' THEN 5
                    WHEN 'Sat' THEN 6
                    ELSE 7
                END,
                start_time
        """, (teacher_id,))
        
        schedule = cursor.fetchall()
        
        # Convert Decimal to float
        result = []
        for item in schedule:
            item_dict = dict(item)
            if 'duration' in item_dict and item_dict['duration']:
                item_dict['duration'] = float(item_dict['duration'])
            result.append(item_dict)
        
        cursor.close()
        return_connection(conn)
        
        return result
        
    except Exception as e:
        print(f"Error fetching schedule: {e}")
        return_connection(conn)
        return []

def update_teacher_profile(teacher_id, username, name, subject, contact, room):
    """อัปเดตข้อมูลโปรไฟล์อาจารย์ รวมทั้ง username"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if new username already exists (for other teachers)
        if username:
            cursor.execute("""
                SELECT id FROM teachers 
                WHERE username = %s AND id != %s
            """, (username, teacher_id))
            
            if cursor.fetchone():
                cursor.close()
                return_connection(conn)
                return False  # Username already taken
        
        # Update profile
        cursor.execute("""
            UPDATE teachers 
            SET username = %s, name = %s, subject = %s, contact = %s, room = %s
            WHERE id = %s
        """, (username, name, subject, contact, room, teacher_id))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error updating teacher profile: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

# ==================== Schedule Functions ====================

def add_schedule(teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color):
    """เพิ่มคาบสอนใหม่"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error adding schedule: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

def update_schedule(schedule_id, day, start_time, end_time, duration, subject, course_code, classroom, color):
    """อัพเดทคาบสอน"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE schedule
            SET day = %s, start_time = %s, end_time = %s, duration = %s, subject = %s, course_code = %s, classroom = %s, color = %s
            WHERE id = %s
        """, (day, start_time, end_time, duration, subject, course_code, classroom, color, schedule_id))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error updating schedule: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

def delete_schedule(schedule_id):
    """ลบคาบสอน"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule WHERE id = %s", (schedule_id,))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

# ==================== Student Functions ====================

def verify_student(username, password):
    """ตรวจสอบข้อมูลนักศึกษา"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM students
            WHERE username = %s AND password = %s
        """, (username, password))
        
        result = cursor.fetchone()
        cursor.close()
        return_connection(conn)
        
        return result is not None
        
    except Exception as e:
        print(f"Error verifying student: {e}")
        return_connection(conn)
        return False

def get_all_teachers_with_schedule():
    """ดึงข้อมูลอาจารย์ทั้งหมดพร้อมตารางสอน (สำหรับนักศึกษา)"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, name, subject, contact, room, profile_picture
            FROM teachers
        """)
        
        teachers = cursor.fetchall()
        
        # ดึงตารางสอนของแต่ละคน
        result = []
        for teacher in teachers:
            teacher_dict = dict(teacher)
            teacher_dict['schedule'] = get_teacher_schedule(teacher_dict['id'])
            teacher_dict['time'] = teacher_dict['contact']
            
            # รวมห้องเรียนจากตารางสอน (unique classrooms)
            classrooms = set()
            for schedule_item in teacher_dict['schedule']:
                if schedule_item.get('classroom'):
                    classrooms.add(schedule_item['classroom'])
            
            # เรียงตามตัวเลข/ตัวอักษรและรวมเป็น string
            if classrooms:
                teacher_dict['classrooms'] = ', '.join(sorted(classrooms))
            else:
                teacher_dict['classrooms'] = '-'
            
            result.append(teacher_dict)
        
        cursor.close()
        return_connection(conn)
        
        return result
        
    except Exception as e:
        print(f"Error fetching all teachers: {e}")
        return_connection(conn)
        return []

def get_all_teacher_schedules():
    """ดึงตารางสอนทั้งหมด (สำหรับนักศึกษา)"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                s.day,
                s.start_time as start,
                s.end_time as end,
                s.duration,
                s.subject,
                s.course_code,
                s.classroom,
                s.color,
                t.name as teacher_name,
                t.room as teacher_room
            FROM schedule s
            JOIN teachers t ON s.teacher_id = t.id
            ORDER BY 
                CASE s.day 
                    WHEN 'Mon' THEN 1
                    WHEN 'Tue' THEN 2
                    WHEN 'Wed' THEN 3
                    WHEN 'Thu' THEN 4
                    WHEN 'Fri' THEN 5
                    WHEN 'Sat' THEN 6
                    ELSE 7
                END,
                s.start_time
        """)
        
        schedules = cursor.fetchall()
        result = [dict(schedule) for schedule in schedules]
        
        cursor.close()
        return_connection(conn)
        
        return result
        
    except Exception as e:
        print(f"Error fetching all schedules: {e}")
        return_connection(conn)
        return []

# ==================== User Management Functions ====================

def get_all_teachers():
    """ดึงรายการอาจารย์ทั้งหมด"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, username, name, subject, contact, room, created_at
            FROM teachers
            ORDER BY created_at DESC
        """)
        
        teachers = cursor.fetchall()
        result = [dict(teacher) for teacher in teachers]
        
        cursor.close()
        return_connection(conn)
        
        return result
        
    except Exception as e:
        print(f"Error fetching teachers: {e}")
        return_connection(conn)
        return []

def get_all_students():
    """ดึงรายการนักศึกษาทั้งหมด"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, username, name, created_at
            FROM students
            ORDER BY created_at DESC
        """)
        
        students = cursor.fetchall()
        result = [dict(student) for student in students]
        
        cursor.close()
        return_connection(conn)
        
        return result
        
    except Exception as e:
        print(f"Error fetching students: {e}")
        return_connection(conn)
        return []

def add_teacher(username, password, name, subject, contact, room):
    """เพิ่มอาจารย์ใหม่"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO teachers (username, password, name, subject, contact, room)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password, name, subject, contact, room))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error adding teacher: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

def add_student(username, password, name):
    """เพิ่มนักศึกษาใหม่"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (username, password, name)
            VALUES (%s, %s, %s)
        """, (username, password, name))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error adding student: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

def delete_teacher(teacher_id):
    """ลบอาจารย์"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error deleting teacher: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

def delete_student(student_id):
    """ลบนักศึกษา"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        
        conn.commit()
        cursor.close()
        return_connection(conn)
        
        return True
        
    except Exception as e:
        print(f"Error deleting student: {e}")
        if conn:
            conn.rollback()
            return_connection(conn)
        return False

# Helper function for database_pwa_helpers.py compatibility
def get_teacher_by_id(teacher_id):
    """Get teacher by ID"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, username, password, name, subject, contact, room, profile_picture
            FROM teachers WHERE id = %s
        """, (teacher_id,))
        
        teacher = cursor.fetchone()
        cursor.close()
        return_connection(conn)
        
        return dict(teacher) if teacher else None
        
    except Exception as e:
        print(f"Error fetching teacher by ID: {e}")
        return_connection(conn)
        return None

def get_student_by_id(student_id):
    """Get student by ID"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, username, password, name
            FROM students WHERE id = %s
        """, (student_id,))
        
        student = cursor.fetchone()
        cursor.close()
        return_connection(conn)
        
        return dict(student) if student else None
        
    except Exception as e:
        print(f"Error fetching student by ID: {e}")
        return_connection(conn)
        return None

def get_student_by_username(username):
    """Get student by username"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, username, password, name
            FROM students WHERE username = %s
        """, (username,))
        
        student = cursor.fetchone()
        cursor.close()
        return_connection(conn)
        
        return dict(student) if student else None
        
    except Exception as e:
        print(f"Error fetching student by username: {e}")
        return_connection(conn)
        return None
