import mysql.connector
from mysql.connector import Error
from database import get_connection

def get_teacher_by_id(teacher_id):
    """Get teacher by ID"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting teacher by ID: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_teacher_by_username(username):
    """Get teacher by username"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teachers WHERE username = %s", (username,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting teacher by username: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_student_by_id(student_id):
    """Get student by ID"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting student by ID: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_student_by_username(username):
    """Get student by username"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error getting student by username: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
