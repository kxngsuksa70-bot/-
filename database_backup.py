import mysql.connector
from mysql.connector import Error
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  # เปลี่ยนเป็นรหัสผ่าน MySQL ของคุณ
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
        # เชื่อมต่อโดยไม่ระบุ database เพื่อสร้าง database
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # สร้างฐานข้อมูล
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
                duration DECIMAL(3,1) NOT NULL,
        teacher_count = cursor.fetchone()[0]
        
        if teacher_count == 0:
            insert_sample_data(conn, cursor)
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"Error initializing database: {e}")
        return False

def insert_sample_data(conn, cursor):
    """เพิ่มข้อมูลตัวอย่าง"""
    try:
        # เพิ่ม teachers
        teachers_data = [
            ("teacher1", "1234", "นางสาวศิริรัตน์ เชื้อแก้ว", "Computer Science", "089-000-1236", "Room 927"),
            ("teacher2", "1234", "Prof. Emily Johnson", "Chemistry", "089-000-1237", "Room 202")
        ]
        
        cursor.executemany("""
            INSERT INTO teachers (username, password, name, subject, contact, room)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, teachers_data)
        
        # เพิ่ม students
        cursor.execute("""
            INSERT INTO students (username, password, name)
            VALUES ('dbt', '1234', 'นักศึกษาทดสอบ')
        """)
        
        # เพิ่ม schedule สำหรับ teacher1
        cursor.execute("SELECT id FROM teachers WHERE username = 'teacher1'")
        teacher1_id = cursor.fetchone()[0]
        
        schedule_data = [
            (teacher1_id, "Mon", "08:00", 1.5, "Intro to Prog", "#4285F4"),
            (teacher1_id, "Wed", "10:00", 2.0, "Database Sys", "#DB4437"),
            (teacher1_id, "Fri", "13:00", 1.5, "Algorithms", "#0F9D58")
        ]
        
        cursor.executemany("""
            INSERT INTO schedule (teacher_id, day, start_time, duration, subject, color)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, schedule_data)
        
        # เพิ่ม schedule สำหรับ teacher2
        cursor.execute("SELECT id FROM teachers WHERE username = 'teacher2'")
        teacher2_id = cursor.fetchone()[0]
        
        schedule_data2 = [
            (teacher2_id, "Tue", "09:00", 1.5, "Organic Chem", "#F4B400"),
            (teacher2_id, "Thu", "11:00", 1.5, "Lab Work", "#4285F4")
        ]

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

def get_teacher_schedule(teacher_id):
    """ดึงตารางสอนของอาจารย์"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, day, start_time as start, duration, subject, color
            FROM schedule WHERE teacher_id = %s
            ORDER BY FIELD(day, 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'), start_time
        """, (teacher_id,))
        
        schedule = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return schedule
        
    except Error as e:
        print(f"Error fetching schedule: {e}")
        return []

def update_teacher_profile(teacher_id, name, subject, contact, room):
    """อัพเดทข้อมูลอาจารย์"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE teachers
            SET name = %s, subject = %s, contact = %s, room = %s
            WHERE id = %s
        """, (name, subject, contact, room, teacher_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error updating teacher profile: {e}")
        return False

# ==================== Schedule Functions ====================

def add_schedule(teacher_id, day, start_time, duration, subject, color):
    """เพิ่มคาบสอนใหม่"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO schedule (teacher_id, day, start_time, duration, subject, color)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (teacher_id, day, start_time, duration, subject, color))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error adding schedule: {e}")
        return False

def update_schedule(schedule_id, day, start_time, duration, subject, color):
    """อัพเดทคาบสอน"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE schedule
            SET day = %s, start_time = %s, duration = %s, subject = %s, color = %s
            WHERE id = %s
        """, (day, start_time, duration, subject, color, schedule_id))
        
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
            SELECT id, name, subject, contact, room
            FROM teachers
        """)
        
        teachers = cursor.fetchall()
        
        # ดึงตารางสอนของแต่ละคน
        for teacher in teachers:
            teacher['schedule'] = get_teacher_schedule(teacher['id'])
            # เปลี่ยน contact เป็น time สำหรับแสดงผล (ใช้ข้อมูลเดิม)
            teacher['time'] = teacher['contact']
        
        cursor.close()
        conn.close()
        
        return teachers
        
    except Error as e:
        print(f"Error fetching all teachers: {e}")
        return []

# ==================== User Management Functions ====================

def add_teacher_user(username, password, name, subject, contact, room):
    """เพิ่มอาจารย์ใหม่"""
    conn = get_connection()
    if not conn:
        return False, "ไม่สามารถเชื่อมต่อฐานข้อมูลได้"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO teachers (username, password, name, subject, contact, room)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password, name, subject, contact, room))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "เพิ่มอาจารย์เรียบร้อยแล้ว"
        
    except Error as e:
        if "Duplicate entry" in str(e):
            return False, f"Username '{username}' ถูกใช้งานแล้ว"
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def add_student_user(username, password, name):
    """เพิ่มนักศึกษาใหม่"""
    conn = get_connection()
    if not conn:
        return False, "ไม่สามารถเชื่อมต่อฐานข้อมูลได้"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (username, password, name)
            VALUES (%s, %s, %s)
        """, (username, password, name))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, "เพิ่มนักศึกษาเรียบร้อยแล้ว"
        
    except Error as e:
        if "Duplicate entry" in str(e):
            return False, f"Username '{username}' ถูกใช้งานแล้ว"
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def get_all_teachers_list():
    """ดึงรายการอาจารย์ทั้งหมด (สำหรับจัดการผู้ใช้)"""
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
        print(f"Error fetching teachers list: {e}")
        return []

def get_all_students_list():
    """ดึงรายการนักศึกษาทั้งหมด (สำหรับจัดการผู้ใช้)"""
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
        print(f"Error fetching students list: {e}")
        return []

# เรียกใช้เมื่อ import module
if __name__ == "__main__":
    init_database()
