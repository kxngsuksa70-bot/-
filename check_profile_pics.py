"""
Check if profile pictures are being saved
"""
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'teachmap_db'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, name, username, profile_picture FROM teachers")
    teachers = cursor.fetchall()
    
    print("Teachers and their profile pictures:")
    print("-" * 60)
    for t in teachers:
        pic = t.get('profile_picture', 'None')
        print(f"ID: {t['id']} | {t['name']} (@{t['username']}) | Pic: {pic}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
