"""
MySQL to Supabase Migration Script
ดูดข้อมูลจาก MySQL และ migrate ไปยัง Supabase PostgreSQL

วิธีใช้:
1. ตรวจสอบว่า MySQL ยังรันอยู่
2. สร้าง .env file ด้วย Supabase credentials
3. รันคำสั่ง: python migrate_mysql_to_supabase.py
"""

# Fix encoding for Windows
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import mysql.connector
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MySQL Configuration (ข้อมูลเดิม)
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  # เปลี่ยนเป็น password ของคุณ
    'database': 'teachmap_db'
}

# Supabase PostgreSQL Configuration (ข้อมูลใหม่)
SUPABASE_CONFIG = {
    'host': os.environ.get('SUPABASE_HOST', 'db.hbbqwcesmwqnfgkmdayp.supabase.co'),
    'port': os.environ.get('SUPABASE_PORT', '5432'),
    'database': os.environ.get('SUPABASE_DB', 'postgres'),
    'user': os.environ.get('SUPABASE_USER', 'postgres'),
    'password': os.environ.get('SUPABASE_PASSWORD', ''),
}

def get_mysql_connection():
    """เชื่อมต่อ MySQL"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print("✅ เชื่อมต่อ MySQL สำเร็จ")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def get_supabase_connection():
    """เชื่อมต่อ Supabase PostgreSQL"""
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        print("✅ เชื่อมต่อ Supabase สำเร็จ")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return None

def migrate_teachers(mysql_conn, supabase_conn):
    """Migrate ตาราง teachers"""
    print("\n📋 กำลัง migrate ตาราง teachers...")
    
    # ดึงข้อมูลจาก MySQL
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    mysql_cursor.execute("""
        SELECT id, username, password, name, subject, contact, room, 
               profile_picture, created_at
        FROM teachers
    """)
    teachers = mysql_cursor.fetchall()
    
    if not teachers:
        print("  ⚠️  ไม่พบข้อมูล teachers")
        return 0
    
    # ใส่ข้อมูลเข้า Supabase
    supabase_cursor = supabase_conn.cursor()
    
    # เตรียมข้อมูล
    values = [
        (
            t['id'], t['username'], t['password'], t['name'],
            t.get('subject'), t.get('contact'), t.get('room'),
            t.get('profile_picture'), t.get('created_at')
        )
        for t in teachers
    ]
    
    # Insert with conflict handling
    execute_values(
        supabase_cursor,
        """
        INSERT INTO teachers 
        (id, username, password, name, subject, contact, room, profile_picture, created_at)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            username = EXCLUDED.username,
            password = EXCLUDED.password,
            name = EXCLUDED.name,
            subject = EXCLUDED.subject,
            contact = EXCLUDED.contact,
            room = EXCLUDED.room,
            profile_picture = EXCLUDED.profile_picture,
            created_at = EXCLUDED.created_at
        """,
        values
    )
    
    supabase_conn.commit()
    print(f"  ✅ Migrate {len(teachers)} teachers สำเร็จ")
    
    mysql_cursor.close()
    supabase_cursor.close()
    
    return len(teachers)

def migrate_students(mysql_conn, supabase_conn):
    """Migrate ตาราง students"""
    print("\n📋 กำลัง migrate ตาราง students...")
    
    # ดึงข้อมูลจาก MySQL
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    mysql_cursor.execute("""
        SELECT id, username, password, name, created_at
        FROM students
    """)
    students = mysql_cursor.fetchall()
    
    if not students:
        print("  ⚠️  ไม่พบข้อมูล students")
        return 0
    
    # ใส่ข้อมูลเข้า Supabase
    supabase_cursor = supabase_conn.cursor()
    
    values = [
        (s['id'], s['username'], s['password'], s['name'], s.get('created_at'))
        for s in students
    ]
    
    execute_values(
        supabase_cursor,
        """
        INSERT INTO students 
        (id, username, password, name, created_at)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            username = EXCLUDED.username,
            password = EXCLUDED.password,
            name = EXCLUDED.name,
            created_at = EXCLUDED.created_at
        """,
        values
    )
    
    supabase_conn.commit()
    print(f"  ✅ Migrate {len(students)} students สำเร็จ")
    
    mysql_cursor.close()
    supabase_cursor.close()
    
    return len(students)

def migrate_schedules(mysql_conn, supabase_conn):
    """Migrate ตาราง schedule"""
    print("\n📋 กำลัง migrate ตาราง schedule...")
    
    # ดึงข้อมูลจาก MySQL
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    mysql_cursor.execute("""
        SELECT id, teacher_id, day, start_time, end_time, duration,
               subject, course_code, classroom, color
        FROM schedule
    """)
    schedules = mysql_cursor.fetchall()
    
    if not schedules:
        print("  ⚠️  ไม่พบข้อมูล schedule")
        return 0
    
    # ใส่ข้อมูลเข้า Supabase
    supabase_cursor = supabase_conn.cursor()
    
    values = [
        (
            s['id'], s['teacher_id'], s['day'], s['start_time'],
            s.get('end_time', ''), float(s['duration']) if s.get('duration') else 0.0,
            s['subject'], s.get('course_code', ''), 
            s.get('classroom', ''), s['color']
        )
        for s in schedules
    ]
    
    execute_values(
        supabase_cursor,
        """
        INSERT INTO schedule 
        (id, teacher_id, day, start_time, end_time, duration, 
         subject, course_code, classroom, color)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            teacher_id = EXCLUDED.teacher_id,
            day = EXCLUDED.day,
            start_time = EXCLUDED.start_time,
            end_time = EXCLUDED.end_time,
            duration = EXCLUDED.duration,
            subject = EXCLUDED.subject,
            course_code = EXCLUDED.course_code,
            classroom = EXCLUDED.classroom,
            color = EXCLUDED.color
        """,
        values
    )
    
    supabase_conn.commit()
    print(f"  ✅ Migrate {len(schedules)} schedules สำเร็จ")
    
    mysql_cursor.close()
    supabase_cursor.close()
    
    return len(schedules)

def reset_sequences(supabase_conn):
    """Reset sequence counters หลัง migrate"""
    print("\n🔧 กำลัง reset sequence counters...")
    
    supabase_cursor = supabase_conn.cursor()
    
    # Reset teachers sequence
    supabase_cursor.execute("""
        SELECT setval('teachers_id_seq', 
            COALESCE((SELECT MAX(id) FROM teachers), 1), true)
    """)
    
    # Reset students sequence
    supabase_cursor.execute("""
        SELECT setval('students_id_seq', 
            COALESCE((SELECT MAX(id) FROM students), 1), true)
    """)
    
    # Reset schedule sequence
    supabase_cursor.execute("""
        SELECT setval('schedule_id_seq', 
            COALESCE((SELECT MAX(id) FROM schedule), 1), true)
    """)
    
    supabase_conn.commit()
    print("  ✅ Reset sequences สำเร็จ")
    
    supabase_cursor.close()

def main():
    """Main migration function"""
    print("=" * 60)
    print("🚀 MySQL → Supabase Migration Tool")
    print("=" * 60)
    
    # เชื่อมต่อ databases
    mysql_conn = get_mysql_connection()
    if not mysql_conn:
        print("\n❌ ไม่สามารถเชื่อมต่อ MySQL ได้ กรุณาตรวจสอบ:")
        print("   - MySQL server รันอยู่หรือไม่")
        print("   - Username/Password ถูกต้องหรือไม่")
        print("   - Database 'teachmap_db' มีอยู่หรือไม่")
        return
    
    supabase_conn = get_supabase_connection()
    if not supabase_conn:
        print("\n❌ ไม่สามารถเชื่อมต่อ Supabase ได้ กรุณาตรวจสอบ:")
        print("   - ไฟล์ .env มี SUPABASE_PASSWORD ถูกต้องหรือไม่")
        print("   - Supabase project รันอยู่หรือไม่")
        print("   - ตารางถูกสร้างแล้วหรือยัง (รัน SETUP_SUPABASE.sql)")
        return
    
    try:
        # เริ่ม migration
        print("\n" + "=" * 60)
        print("📦 เริ่ม Migration")
        print("=" * 60)
        
        teachers_count = migrate_teachers(mysql_conn, supabase_conn)
        students_count = migrate_students(mysql_conn, supabase_conn)
        schedules_count = migrate_schedules(mysql_conn, supabase_conn)
        
        # Reset sequences
        reset_sequences(supabase_conn)
        
        # สรุปผล
        print("\n" + "=" * 60)
        print("✅ Migration เสร็จสมบูรณ์!")
        print("=" * 60)
        print(f"📊 สรุปข้อมูลที่ migrate:")
        print(f"   - Teachers:  {teachers_count} รายการ")
        print(f"   - Students:  {students_count} รายการ")
        print(f"   - Schedules: {schedules_count} รายการ")
        print(f"   - รวม:       {teachers_count + students_count + schedules_count} รายการ")
        print("\n🎉 ข้อมูลทั้งหมดถูก migrate ไปยัง Supabase แล้ว!")
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดระหว่าง migration: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # ปิดการเชื่อมต่อ
        if mysql_conn:
            mysql_conn.close()
            print("\n🔌 ปิดการเชื่อมต่อ MySQL")
        if supabase_conn:
            supabase_conn.close()
            print("🔌 ปิดการเชื่อมต่อ Supabase")

if __name__ == '__main__':
    main()
