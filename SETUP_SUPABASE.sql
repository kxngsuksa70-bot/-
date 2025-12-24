-- ========================================
-- TeachMap PWA - Supabase Schema Setup
-- ========================================
-- Instructions:
-- 1. Go to: https://supabase.com/dashboard/project/hbbqwcesmwqnfgkmdayp
-- 2. Click "SQL Editor" in the left sidebar
-- 3. Click "New query"
-- 4. Copy and paste this ENTIRE file
-- 5. Click "Run" (or press Ctrl+Enter)
-- 6. Done! Your tables are ready!
-- ========================================

-- ========================================
-- ENCODING: ตั้งค่า UTF-8 สำหรับภาษาไทย
-- ========================================
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- ========================================
-- STEP 1: สร้างตารางหลัก (Teachers & Students)
-- ========================================

-- ตาราง teachers - เก็บข้อมูลอาจารย์
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

-- ตาราง students - เก็บข้อมูลนักศึกษา
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- STEP 2: สร้างตารางตารางสอน (เชื่อมกับ teachers)
-- ========================================

-- ตาราง schedule - เก็บตารางสอน
-- ⚡ เชื่อมกับ teachers ผ่าน teacher_id (Foreign Key)
CREATE TABLE IF NOT EXISTS schedule (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER NOT NULL,                    -- เชื่อมกับ teachers.id
    day VARCHAR(10) NOT NULL,
    start_time VARCHAR(10) NOT NULL,
    end_time VARCHAR(10) DEFAULT '',
    duration DECIMAL(3,1) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) DEFAULT '',
    classroom VARCHAR(50) DEFAULT '',
    color VARCHAR(20) NOT NULL,
    
    -- 🔗 Foreign Key: เชื่อมกับตาราง teachers
    -- ถ้าลบ teacher จะลบ schedule ทั้งหมดของ teacher นั้นด้วย (ON DELETE CASCADE)
    CONSTRAINT fk_schedule_teacher 
        FOREIGN KEY (teacher_id) 
        REFERENCES teachers(id) 
        ON DELETE CASCADE
);

-- ========================================
-- STEP 3: เพิ่มข้อมูลตัวอย่าง
-- ========================================

-- เพิ่มอาจารย์ตัวอย่าง
INSERT INTO teachers (username, password, name, subject, contact, room) VALUES
('teacher1', '1234', 'นางสาวศิริรัตน์ เชื้อแก้ว', 'Computer Science', '089-000-1236', 'Room 927'),
('teacher2', '1234', 'Prof. Emily Johnson', 'Chemistry', '089-000-1237', 'Room 202')
ON CONFLICT (username) DO NOTHING;

-- เพิ่มนักศึกษาตัวอย่าง
INSERT INTO students (username, password, name) VALUES
('student1', '1234', 'นักศึกษาทดสอบ')
ON CONFLICT (username) DO NOTHING;

-- เพิ่มตารางสอนสำหรับ teacher1 (id=1)
-- 🔗 teacher_id = 1 เชื่อมกับ teachers.id = 1
INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color) VALUES
(1, 'Mon', '08:30', '10:00', 1.5, 'Intro to Prog', 'CS101', '927', '#4285F4'),
(1, 'Wed', '12:30', '14:30', 2.0, 'Database Sys', 'CS201', '925', '#DB4437'),
(1, 'Fri', '08:30', '10:00', 1.5, 'Algorithms', 'CS301', '927', '#0F9D58')
ON CONFLICT DO NOTHING;

-- เพิ่มตารางสอนสำหรับ teacher2 (id=2)
-- 🔗 teacher_id = 2 เชื่อมกับ teachers.id = 2
INSERT INTO schedule (teacher_id, day, start_time, end_time, duration, subject, course_code, classroom, color) VALUES
(2, 'Tue', '08:30', '10:00', 1.5, 'Organic Chem', 'CHEM201', '925', '#F4B400'),
(2, 'Thu', '13:30', '15:00', 1.5, 'Lab Work', 'CHEM202', '925', '#4285F4')
ON CONFLICT DO NOTHING;

-- ========================================
-- STEP 4: สร้าง Indexes เพื่อเพิ่มความเร็ว
-- ========================================

CREATE INDEX IF NOT EXISTS idx_schedule_teacher ON schedule(teacher_id);
CREATE INDEX IF NOT EXISTS idx_schedule_day ON schedule(day);
CREATE INDEX IF NOT EXISTS idx_teachers_username ON teachers(username);
CREATE INDEX IF NOT EXISTS idx_students_username ON students(username);

-- ========================================
-- STEP 5: แสดงผลลัพธ์
-- ========================================

SELECT 'Database setup complete! ✅' as status;
SELECT 'Teachers: ' || COUNT(*)::text FROM teachers;
SELECT 'Students: ' || COUNT(*)::text FROM students;
SELECT 'Schedules: ' || COUNT(*)::text FROM schedule;

-- ========================================
-- โครงสร้างความสัมพันธ์:
-- ========================================
-- teachers (1) ----< schedule (Many)
--   └─ หน่ึง teacher มีหลาย schedule items
--   └─ schedule.teacher_id → teachers.id (Foreign Key)
--
-- students (ไม่มีความสัมพันธ์โดยตรง)
--   └─ ใช้สำหรับ login เท่านั้น
-- ========================================
