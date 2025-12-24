# Supabase PostgreSQL Schema
# Run this in Supabase SQL Editor

-- สร้างตาราง teachers
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
);

-- สร้างตาราง students
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- สร้างตาราง schedule
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
);

-- เพิ่มข้อมูลตัวอย่าง teachers (optional - สำหรับทดสอบ)
INSERT INTO teachers (username, password, name, subject, contact, room) VALUES
('teacher1', '1234', 'นางสาวศิริรัตน์ เชื้อแก้ว', 'Computer Science', '089-000-1236', 'Room 927'),
('teacher2', '1234', 'Prof. Emily Johnson', 'Chemistry', '089-000-1237', 'Room 202');

-- เพิ่มข้อมูลตัวอย่าง students
INSERT INTO students (username, password, name) VALUES
('student1', '1234', 'นักศึกษาทดสอบ');

-- เพิ่มข้อมูลตัวอย่าง schedule สำหรับ teacher1
INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color) VALUES
(1, 'Mon', '08:30', '10:00', 1.5, 'Intro to Prog', 'CS101', '927', '#4285F4'),
(1, 'Wed', '12:30', '14:30', 2.0, 'Database Sys', 'CS201', '925', '#DB4437'),
(1, 'Fri', '08:30', '10:00', 1.5, 'Algorithms', 'CS301', '927', '#0F9D58');

-- เพิ่มข้อมูลตัวอย่าง schedule สำหรับ teacher2
INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color) VALUES
(2, 'Tue', '08:30', '10:00', 1.5, 'Organic Chem', 'CHEM201', '925', '#F4B400'),
(2, 'Thu', '13:30', '15:00', 1.5, 'Lab Work', 'CHEM202', '925', '#4285F4');

-- สร้าง index เพื่อเพิ่มประสิทธิภาพ
CREATE INDEX IF NOT EXISTS idx_schedule_teacher ON schedule(teacher_id);
CREATE INDEX IF NOT EXISTS idx_schedule_day ON schedule(day);
CREATE INDEX IF NOT EXISTS idx_teachers_username ON teachers(username);
CREATE INDEX IF NOT EXISTS idx_students_username ON students(username);
