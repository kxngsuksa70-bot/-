import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('teachmap.db')
        cursor = conn.cursor()
        
        print("--- Teachers ---")
        cursor.execute("SELECT id, username, password FROM teachers")
        teachers = cursor.fetchall()
        for t in teachers:
            print(f"ID: {t[0]}, User: {t[1]}, Pass: {t[2]}")
            
        if not teachers:
            print("No teachers found!")
            
        print("\n--- Students ---")
        cursor.execute("SELECT id, username, password FROM students")
        students = cursor.fetchall()
        for s in students:
            print(f"ID: {s[0]}, User: {s[1]}, Pass: {s[2]}")

        if not students:
            print("No students found!")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_db()
