from database_supabase import get_supabase_client

def get_teacher_by_id(teacher_id):
    """Get teacher by ID"""
    try:
        client = get_supabase_client()
        response = client.table('teachers').select('*').eq('id', teacher_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting teacher by ID: {e}")
        return None

def get_teacher_by_username(username):
    """Get teacher by username"""
    try:
        client = get_supabase_client()
        response = client.table('teachers').select('*').eq('username', username).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting teacher by username: {e}")
        return None

def get_student_by_id(student_id):
    """Get student by ID"""
    try:
        client = get_supabase_client()
        response = client.table('students').select('*').eq('id', student_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return None

def get_student_by_username(username):
    """Get student by username"""
    try:
        client = get_supabase_client()
        response = client.table('students').select('*').eq('username', username).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting student by username: {e}")
        return None
