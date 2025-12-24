def update_teacher_profile(teacher_id, username, name, subject, contact, room):
    """อัปเดตข้อมูลโปรไฟล์อาจารย์ รวมทั้ง username"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if new username already exists (for other teachers)
        if username:
            cursor.execute("""
                SELECT id FROM teachers 
                WHERE username = %s AND id != %s
            """, (username, teacher_id))
            
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False  # Username already taken
        
        # Update profile
        cursor.execute("""
            UPDATE teachers 
            SET username = %s, name = %s, subject = %s, contact = %s, room = %s
            WHERE id = %s
        """, (username, name, subject, contact, room, teacher_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Error as e:
        print(f"Error updating teacher profile: {e}")
        return False
