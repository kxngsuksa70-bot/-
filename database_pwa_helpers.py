import psycopg2
from psycopg2 import Error
from database_postgres import get_connection

def get_teacher_by_id(teacher_id):
    """Get teacher by ID"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        from psycopg2.extras import RealDictCursor
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting teacher by ID: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_teacher_by_username(username):
    """Get teacher by username"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        from psycopg2.extras import RealDictCursor
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM teachers WHERE username = %s", (username,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting teacher by username: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_student_by_id(student_id):
    """Get student by ID"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        from psycopg2.extras import RealDictCursor
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting student by ID: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_student_by_username(username):
    """Get student by username"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        from psycopg2.extras import RealDictCursor
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting student by username: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()
