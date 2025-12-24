import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
import database as db
import database_pwa_helpers as db_helpers

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'teachmap_secret_key_2024'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

class User(UserMixin):
    def __init__(self, id, username, role, data=None):
        self.id = id
        self.username = username
        self.role = role
        self.data = data or {}

@login_manager.user_loader
def load_user(user_id):
    if ':' not in user_id:
        return None
    
    role, uid = user_id.split(':', 1)
    if role == 'teacher':
        teacher = db_helpers.get_teacher_by_id(int(uid))
        if teacher:
            return User(user_id, teacher['username'], 'teacher', teacher)
    elif role == 'student':
        student = db_helpers.get_student_by_id(int(uid))
        if student:
            return User(user_id, student['username'], 'student', student)
    return None

def role_required(role):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ============== ROUTES ==============

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/student')
@login_required
def student_page():
    if current_user.role != 'student':
        return send_from_directory('static', 'index.html')
    return send_from_directory('static', 'student.html')

@app.route('/teacher')
@login_required
def teacher_page():
    if current_user.role != 'teacher':
        return send_from_directory('static', 'index.html')
    return send_from_directory('static', 'teacher.html')

# ============== API ENDPOINTS ==============

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'student')
    
    if role == 'teacher':
        if db.verify_teacher(username, password):
            teacher = db_helpers.get_teacher_by_username(username)
            if teacher:
                user = User(f"teacher:{teacher['id']}", username, 'teacher', teacher)
                login_user(user)
                return jsonify({
                    'success': True,
                    'role': 'teacher',
                    'redirect': '/teacher-dashboard.html',
                    'user': {
                        'id': teacher['id'],
                        'name': teacher['name'],
                        'username': teacher['username']
                    }
                })
    elif role == 'student':
        if db.verify_student(username, password):
            student = db_helpers.get_student_by_username(username)
            if student:
                user = User(f"student:{student['id']}", username, 'student', student)
                login_user(user)
                return jsonify({
                    'success': True,
                    'role': 'student',
                    'redirect': '/student',
                    'user': {
                        'id': student['id'],
                        'name': student['name'],
                        'username': student['username']
                    }
                })
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'success': True})

@app.route('/api/teachers')
def api_teachers():
    teachers = db.get_all_teachers_with_schedule()
    return jsonify(teachers)

@app.route('/api/teachers/<int:teacher_id>/schedule')
def api_teacher_full_schedule(teacher_id):
    schedule = db.get_teacher_schedule(teacher_id)
    teacher = db.get_teacher_by_id(teacher_id)
    return jsonify({'teacher': teacher, 'schedule': schedule})

# Student Dashboard - Get all schedules
@app.route('/api/all-schedules')
def api_all_schedules():
    all_schedules = db.get_all_teacher_schedules()
    return jsonify(all_schedules)

# Teacher Schedule Management
@app.route('/api/schedule', methods=['GET'])
@role_required('teacher')
def api_my_schedule():
    teacher_id = current_user.data.get('id')
    schedule = db.get_teacher_schedule(teacher_id)
    return jsonify(schedule)

@app.route('/api/schedule', methods=['POST'])
@role_required('teacher')
def api_add_schedule():
    data = request.get_json()
    teacher_id = current_user.data.get('id')
    
    result = db.add_schedule(
        teacher_id,
        data['day'],
        data['start_time'],
        data['end_time'],
        data['duration'],
        data['subject'],
        data.get('course_code', ''),
        data.get('classroom', ''),
        data.get('color', '#4285F4')
    )
    
    if result:
        return jsonify({'success': True, 'message': 'Schedule added'})
    return jsonify({'success': False, 'error': 'Failed to add schedule'}), 400

@app.route('/api/schedule/<int:schedule_id>', methods=['PUT'])
@role_required('teacher')
def api_update_schedule(schedule_id):
    data = request.get_json()
    
    result = db.update_schedule(
        schedule_id,
        data['day'],
        data['start_time'],
        data['end_time'],
        data['duration'],
        data['subject'],
        data.get('course_code', ''),
        data.get('classroom', ''),
        data.get('color', '#4285F4')
    )
    
    if result:
        return jsonify({'success': True, 'message': 'Schedule updated'})
    return jsonify({'success': False, 'error': 'Failed to update schedule'}), 400

@app.route('/api/schedule/<int:schedule_id>', methods=['DELETE'])
@role_required('teacher')
def api_delete_schedule(schedule_id):
    result = db.delete_schedule(schedule_id)
    if result:
        return jsonify({'success': True, 'message': 'Schedule deleted'})
    return jsonify({'success': False, 'error': 'Failed to delete schedule'}), 400

# User Management
@app.route('/api/users/students')
@role_required('teacher')
def api_get_students():
    students = db.get_all_students()
    return jsonify(students)

@app.route('/api/users/teachers')
@role_required('teacher')
def api_get_teachers():
    teachers = db.get_all_teachers()
    return jsonify(teachers)

# Admin User Management
@app.route('/api/admin/teachers', methods=['POST'])
@role_required('teacher')
def api_add_teacher():
    data = request.get_json()
    result = db.add_teacher(
        data['username'],
        data['password'],
        data['name'],
        data.get('subject', ''),
        data.get('contact', ''),
        data.get('room', '')
        data['username'],
        data['password'],
        data['name']
    
    if request.method == 'GET':
        teacher = db_helpers.get_teacher_by_id(int(user.id.split(':')[1]))
        if teacher:
            return jsonify(teacher)
        return jsonify({'success': False, 'error': 'Teacher not found'}), 404
    
    elif request.method == 'PUT':
        data = request.get_json()
        teacher_id = int(user.id.split(':')[1])
        result = db.update_teacher_profile(
            teacher_id,
            data.get('username'),
            data.get('name'),
            data.get('subject'),
            data.get('contact'),
            data.get('room')
        )
        if result:
            # Update localStorage with new username
            return jsonify({
                'success': True, 
                'message': 'Profile updated',
                'username': data.get('username')
            })
        return jsonify({'success': False, 'error': 'Failed to update profile or username already taken'}), 400

if __name__ == '__main__':
    print("=== TeachMap PWA Server Starting ===")
    print("Mobile access: http://<your-ip>:5000")
    print("Desktop access: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
