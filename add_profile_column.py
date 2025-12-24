"""
Add profile_picture column to teachers table
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
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'teachmap_db' 
        AND TABLE_NAME = 'teachers' 
        AND COLUMN_NAME = 'profile_picture'
    """)
    
    exists = cursor.fetchone()[0]
    
    if exists:
        print("[OK] Column 'profile_picture' already exists in teachers table")
    else:
        # Add column
        cursor.execute("ALTER TABLE teachers ADD COLUMN profile_picture VARCHAR(255)")
        conn.commit()
        print("[OK] Successfully added column 'profile_picture' to teachers table")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
