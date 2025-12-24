"""
Database Migration Script - Add Missing Columns to Schedule Table
This script will:
1. Add classroom, course_code, and end_time columns to existing schedule table
2. Update existing schedule records with sample classroom data
"""

import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'teachmap_db'
}

def migrate_database():
    """Run database migration to add missing columns"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔄 Starting database migration...")
        
        # Check if columns already exist
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'teachmap_db' 
            AND TABLE_NAME = 'schedule'
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"✅ Existing columns: {existing_columns}")
        
        # Add missing columns
        if 'end_time' not in existing_columns:
            print("📝 Adding end_time column...")
            cursor.execute("""
                ALTER TABLE schedule 
                ADD COLUMN end_time VARCHAR(10) DEFAULT '' AFTER start_time
            """)
            
        if 'course_code' not in existing_columns:
            print("📝 Adding course_code column...")
            cursor.execute("""
                ALTER TABLE schedule 
                ADD COLUMN course_code VARCHAR(50) DEFAULT '' AFTER subject
            """)
            
        if 'classroom' not in existing_columns:
            print("📝 Adding classroom column...")
            cursor.execute("""
                ALTER TABLE schedule 
                ADD COLUMN classroom VARCHAR(50) DEFAULT '' AFTER course_code
            """)
        
        conn.commit()
        print("✅ Schema updated successfully!")
        
        # Update existing schedule records with sample data
        print("\n🔄 Updating existing schedule with classroom data...")
        
        # Get all schedule items
        cursor.execute("SELECT id, subject, start_time, duration FROM schedule")
        schedules = cursor.fetchall()
        
        # Sample classroom assignments
        classroom_map = {
            'Intro to Prog': ('927', 'CS101'),
            'Database Sys': ('925', 'CS201'),
            'Algorithms': ('927', 'CS301'),
            'Organic Chem': ('925', 'CHEM201'),
            'Lab Work': ('925', 'CHEM202')
        }
        
        for schedule_id, subject, start_time, duration in schedules:
            if subject in classroom_map:
                classroom, course_code = classroom_map[subject]
                
                # Calculate end_time from start_time and duration
                start_h, start_m = map(int, start_time.split(':'))
                total_minutes = start_h * 60 + start_m + int(float(duration) * 60)
                end_h = total_minutes // 60
                end_m = total_minutes % 60
                end_time = f"{end_h:02d}:{end_m:02d}"
                
                cursor.execute("""
                    UPDATE schedule 
                    SET classroom = %s, course_code = %s, end_time = %s
                    WHERE id = %s
                """, (classroom, course_code, end_time, schedule_id))
                
                print(f"  ✅ Updated {subject}: room {classroom}, code {course_code}, time {start_time}-{end_time}")
        
        conn.commit()
        print("\n🎉 Migration completed successfully!")
        print("✅ All schedule items now have classroom information")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Migration error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("TeachMap Database Migration")
    print("=" * 60)
    migrate_database()
