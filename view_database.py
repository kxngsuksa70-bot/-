import database as db

# เชื่อมต่อ database
conn = db.get_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    print("=" * 60)
    print("ตาราง TEACHERS")
    print("=" * 60)
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    for t in teachers:
        print(f"ID: {t['id']}, Username: {t['username']}, Name: {t['name']}")
        print(f"   Subject: {t['subject']}, Room: {t['room']}, Contact: {t['contact']}")
        print()
    
    print("=" * 60)
    print("ตาราง SCHEDULE")
    print("=" * 60)
    cursor.execute("""
        SELECT s.*, t.name as teacher_name 
        FROM schedule s 
        JOIN teachers t ON s.teacher_id = t.id
    """)
    schedules = cursor.fetchall()
    for s in schedules:
        print(f"ID: {s['id']}, Teacher: {s['teacher_name']}")
        print(f"   {s['day']} {s['start_time']} - {s['subject']} ({s['duration']}h)")
        print()
    
    print("=" * 60)
    print("ตาราง STUDENTS")
    print("=" * 60)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    for st in students:
        print(f"ID: {st['id']}, Username: {st['username']}, Name: {st['name']}")
    
    cursor.close()
    conn.close()
else:
    print("ไม่สามารถเชื่อมต่อ database ได้")
