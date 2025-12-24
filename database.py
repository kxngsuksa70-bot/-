import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'teachmap_db'
}

def get_connection():
    """สร้างและคืนค่า MySQL connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    """สร้างฐานข้อมูลและตารางถ้ายังไม่มี"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # สร้างตาราง teachers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                subject VARCHAR(255),
                contact VARCHAR(50),
                room VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # สร้างตาราง students
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # สร้างตาราง schedule
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INT AUTO_INCREMENT PRIMARY KEY,
                teacher_id INT NOT NULL,
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
            # เพิ่มข้อมูลตัวอย่าง
            cursor.executemany("""
                INSERT INTO teachers (username, password, name, subject, contact, room)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [
                ("teacher1", "1234", "นางสาวศิริรัตน์ เชื้อแก้ว", "Computer Science", "089-000-1236", "Room 927"),
                ("teacher2", "1234", "Prof. Emily Johnson", "Chemistry", "089-000-1237", "Room 202")
            ])
            
            cursor.execute("INSERT INTO students (username, password, name) VALUES ('student1', '1234', 'นักศึกษาทดสอบ')")
            
            cursor.execute("SELECT id FROM teachers WHERE username = 'teacher1'")
            t1 = cursor.fetchone()[0]
            cursor.executemany("""
                INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                (t1, "Mon", "08:30", "10:00", 1.5, "Intro to Prog", "CS101", "927", "#4285F4"),
                (t1, "Wed", "12:30", "14:30", 2.0, "Database Sys", "CS201", "925", "#DB4437"),
                (t1, "Fri", "08:30", "10:00", 1.5, "Algorithms", "CS301", "927", "#0F9D58")
            ])
            
            cursor.execute("SELECT id FROM teachers WHERE username = 'teacher2'")
            t2 = cursor.fetchone()[0]
            cursor.executemany("""
                INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                (t2, "Tue", "08:30", "10:00", 1.5, "Organic Chem", "CHEM201", "925", "#F4B400"),
                (t2, "Thu", "13:30", "15:00", 1.5, "Lab Work", "CHEM202", "925", "#4285F4")
            ])
            
            conn.commit()
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"Error initializing database: {e}")
        return False

# ==================== Teacher Functions ====================

def get_teacher_by_username(username):
    """ดึงข้อมูลอาจารย์จาก username"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, password, name, subject, contact, room
            FROM teachers WHERE username = %s
        """, (username,))
        
        teacher = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return teacher
        
    except Error as e:
        print(f"Error fetching teacher: {e}")
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
        conn.close()
        
        return result is not None
        
    except Error as e:
        print(f"Error verifying teacher: {e}")
        return False

def get_teacher_schedule(teacher_id):
    """ดึงตารางสอนของอาจารย์"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, day, start_time as start, end_time as end, duration, subject, course_code, classroom, color
            FROM schedule WHERE teacher_id = %s
            ORDER BY FIELD(day, 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'), start_time
        """, (teacher_id,))
        
        schedule = cursor.fetchall()
        
        # Convert Decimal to float
        for item in schedule:
            if 'duration' in item and item['duration']:
                item['duration'] = float(item['duration'])
        
        cursor.close()
        conn.close()
        
        return schedule
        
    except Error as e:
        print(f"Error fetching schedule: {e}")
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
                conn.close()
                return False  # Username already taken
        
        # Update profile
        cursor.execute("""
            UPDATE teachers 
            SET username = %s, name = %s, subject = %s, contact = %s, room = %s
            WHERE id = %s
        """, (username, name, subject, contact, room, teacher_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error updating teacher profile: {e}")
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
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error adding schedule: {e}")
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
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error updating schedule: {e}")
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
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error deleting schedule: {e}")
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
        conn.close()
        
        return result is not None
        
    except Error as e:
        print(f"Error verifying student: {e}")
        return False

def get_all_teachers_with_schedule():
    """ดึงข้อมูลอาจารย์ทั้งหมดพร้อมตารางสอน (สำหรับนักศึกษา)"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, subject, contact, room, profile_picture
            FROM teachers
        """)
        
        teachers = cursor.fetchall()
        
        # ดึงตารางสอนของแต่ละคน
        for teacher in teachers:
            teacher['schedule'] = get_teacher_schedule(teacher['id'])
            teacher['time'] = teacher['contact']
            
            # รวมห้องเรียนจากตารางสอน (unique classrooms)
            classrooms = set()
            for schedule_item in teacher['schedule']:
                if schedule_item.get('classroom'):
                    classrooms.add(schedule_item['classroom'])
            
            # เรียงตามตัวเลข/ตัวอักษรและรวมเป็น string
            if classrooms:
                teacher['classrooms'] = ', '.join(sorted(classrooms))
            else:
                teacher['classrooms'] = '-'
        
        cursor.close()
        conn.close()
        
        return teachers
        
    except Error as e:
        print(f"Error fetching all teachers: {e}")
        return []

def get_all_teacher_schedules():
    """ดึงตารางสอนทั้งหมด (สำหรับนักศึกษา)"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
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
            ORDER BY FIELD(s.day, 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'), s.start_time
        """)
        
        schedules = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return schedules
        
    except Error as e:
        print(f"Error fetching all schedules: {e}")
        return []

# ==================== User Management Functions ====================

def get_all_teachers():
    """ดึงรายการอาจารย์ทั้งหมด"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, name, subject, contact, room, created_at
            FROM teachers
            ORDER BY created_at DESC
        """)
        
        teachers = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return teachers
        
    except Error as e:
        print(f"Error fetching teachers: {e}")
        return []

def get_all_students():
    """ดึงรายการนักศึกษาทั้งหมด"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, name, created_at
            FROM students
            ORDER BY created_at DESC
        """)
        
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return students
        
    except Error as e:
        print(f"Error fetching students: {e}")
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
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error adding teacher: {e}")
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
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error adding student: {e}")
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
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error deleting teacher: {e}")
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
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error deleting student: {e}")
        return False
