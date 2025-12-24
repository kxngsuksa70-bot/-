-- สร้างฐานข้อมูล
CREATE DATABASE IF NOT EXISTS teachmap_db;
USE teachmap_db;

-- สร้างตาราง teachers
CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    contact VARCHAR(50),
    room VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- สร้างตาราง students
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- สร้างตาราง schedule
CREATE TABLE IF NOT EXISTS schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    day VARCHAR(10) NOT NULL,
    start_time VARCHAR(10) NOT NULL,
    duration DECIMAL(3,1) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    color VARCHAR(20) NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
);

-- เพิ่มข้อมูลตัวอย่าง teachers
INSERT INTO teachers (username, password, name, subject, contact, room) VALUES
('teacher1', '1234', 'นางสาวศิริรัตน์ เชื้อแก้ว', 'Computer Science', '089-000-1236', 'Room 927'),
('teacher2', '1234', 'Prof. Emily Johnson', 'Chemistry', '089-000-1237', 'Room 202');

-- เพิ่มข้อมูลตัวอย่าง students
INSERT INTO students (username, password, name) VALUES
('student1', '1234', 'นักศึกษาทดสอบ');

-- เพิ่มข้อมูลตัวอย่าง schedule สำหรับ teacher1
INSERT INTO schedule (teacher_id, day, start_time, duration, subject, color) VALUES
(1, 'Mon', '08:00', 1.5, 'Intro to Programming', '#4285F4'),
(1, 'Wed', '10:00', 2.0, 'Database Systems', '#DB4437'),
(1, 'Fri', '13:00', 1.5, 'Algorithms', '#0F9D58');

-- เพิ่มข้อมูลตัวอย่าง schedule สำหรับ teacher2
INSERT INTO schedule (teacher_id, day, start_time, duration, subject, color) VALUES
(2, 'Tue', '09:00', 1.5, 'Organic Chemistry', '#F4B400'),
(2, 'Thu', '11:00', 1.5, 'Lab Work', '#4285F4');
