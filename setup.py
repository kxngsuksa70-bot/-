#!/usr/bin/env python3
"""
Setup script to initialize the TeachMap database with tables and sample data.
Run this script once before using the application.

Usage:
    python setup.py
"""

import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
}

DB_NAME = "teachmap"

def create_database():
    """Create the database if it doesn't exist"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' created or already exists.")
        
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables"""
    try:
        config = {**DB_CONFIG, "database": DB_NAME}
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Teachers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                subject VARCHAR(100),
                contact VARCHAR(50),
                room VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'teachers' created.")
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'students' created.")
        
        # Schedule table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INT AUTO_INCREMENT PRIMARY KEY,
                teacher_id INT NOT NULL,
                day VARCHAR(10) NOT NULL,
                start_time VARCHAR(10) NOT NULL,
                duration FLOAT NOT NULL,
                subject VARCHAR(100) NOT NULL,
                color VARCHAR(10) DEFAULT '#4285F4',
                FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
            )
        """)
        print("✅ Table 'schedule' created.")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_sample_data():
    """Insert sample teachers, students, and schedules"""
    try:
        config = {**DB_CONFIG, "database": DB_NAME}
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM teachers")
        if cursor.fetchone()[0] > 0:
            print("⚠️  Sample data already exists. Skipping insertion.")
            cursor.close()
            conn.close()
            return True
        
        # Insert sample teachers
        teachers = [
            ('teacher1', '1234', 'นางสาวศิริรัตน์ เชื้อแก้ว', 'Computer Science', '089-000-1236', 'ห้อง 927'),
            ('teacher2', '1234', 'Prof. Emily Johnson', 'Chemistry', '089-000-1237', 'Room 202'),
        ]
        
        cursor.executemany(
            "INSERT INTO teachers (username, password, name, subject, contact, room) VALUES (%s, %s, %s, %s, %s, %s)",
            teachers
        )
        print(f"✅ Inserted {cursor.rowcount} sample teachers.")
        
        # Insert sample students
        students = [
            ('student1', '1234', 'นายสมชาย ใจดี'),
            ('student2', '1234', 'นางสาวสมหญิง รักเรียน'),
        ]
        
        cursor.executemany(
            "INSERT INTO students (username, password, name) VALUES (%s, %s, %s)",
            students
        )
        print(f"✅ Inserted {cursor.rowcount} sample students.")
        
        # Insert sample schedules for teacher1 (id=1)
        schedules = [
            (1, 'Mon', '08:00', 1.5, 'Intro to Programming', '#4285F4'),
            (1, 'Wed', '10:00', 2.0, 'Database Systems', '#DB4437'),
            (1, 'Fri', '13:00', 1.5, 'Algorithms', '#0F9D58'),
            (2, 'Tue', '09:00', 1.5, 'Organic Chemistry', '#F4B400'),
            (2, 'Thu', '11:00', 1.5, 'Lab Work', '#4285F4'),
        ]
        
        cursor.executemany(
            "INSERT INTO schedule (teacher_id, day, start_time, duration, subject, color) VALUES (%s, %s, %s, %s, %s, %s)",
            schedules
        )
        print(f"✅ Inserted {cursor.rowcount} sample schedules.")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("TeachMap Database Setup")
    print("=" * 50)
    print()
    
    print("Step 1: Creating database...")
    if not create_database():
        return
    print()
    
    print("Step 2: Creating tables...")
    if not create_tables():
        return
    print()
    
    print("Step 3: Inserting sample data...")
    if not insert_sample_data():
        return
    print()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("=" * 50)
    print()
    print("Sample login credentials:")
    print("  Teacher: username='teacher1', password='1234'")
    print("  Student: username='student1', password='1234'")
    print()
    print("You can now run: python coppy.py")

if __name__ == "__main__":
    main()
