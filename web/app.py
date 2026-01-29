import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, session, send_from_directory, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from functools import wraps
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import qrcode
from io import BytesIO

# Load environment variables
load_dotenv()

# Import Supabase database (REST API - works with Railway)
import database_supabase as db
import database_pwa_helpers as db_helpers

app = Flask(__name__, static_folder='static', static_url_path='')

# Configuration from environment variables
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# CORS configuration
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'images', 'profiles')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

# Custom unauthorized handler to return JSON instead of redirecting
@login_manager.unauthorized_handler
def unauthorized():
    # Check if request is API call (wants JSON)
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Authentication required. Please log in first.'}), 401
    # Otherwise redirect to login page
    return redirect(url_for('index'))

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
        # ⚡ Real-time update: notify all clients
        socketio.emit('schedule_updated', {'action': 'add'}, namespace='/')
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
        # ⚡ Real-time update: notify all clients
        socketio.emit('schedule_updated', {'action': 'update'}, namespace='/')
        return jsonify({'success': True, 'message': 'Schedule updated'})
    return jsonify({'success': False, 'error': 'Failed to update schedule'}), 400

@app.route('/api/schedule/<int:schedule_id>', methods=['DELETE'])
@role_required('teacher')
def api_delete_schedule(schedule_id):
    result = db.delete_schedule(schedule_id)
    if result:
        # ⚡ Real-time update: notify all clients
        socketio.emit('schedule_updated', {'action': 'delete'}, namespace='/')
        return jsonify({'success': True, 'message': 'Schedule deleted'})
    return jsonify({'success': False, 'error': 'Failed to delete schedule'}), 400

# Profile Picture Upload (Supabase Storage)
@app.route('/api/upload_profile_picture', methods=['POST'])
@role_required('teacher')
def api_upload_profile_picture():
    """Upload profile picture to Supabase Storage"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'success': False, 'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'}), 400
    
    try:
        teacher_id = current_user.data.get('id')
        
        # Generate unique filename
        import uuid
        import os as os_module
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"teacher_{teacher_id}_{uuid.uuid4().hex}.{ext}"
        
        # Read file content
        file_content = file.read()
        
        # Upload to Supabase Storage
        client = db.get_supabase_client()
        storage_response = client.storage.from_('profile-pictures').upload(
            path=filename,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        
        # Get public URL
        public_url = client.storage.from_('profile-pictures').get_public_url(filename)
        
        # Update teacher profile with new picture URL
        client.table('teachers').update({
            'profile_picture': public_url
        }).eq('id', teacher_id).execute()
        
        return jsonify({
            'success': True,
            'message': 'Profile picture uploaded successfully',
            'url': public_url
        })
        
    except Exception as e:
        print(f"Error uploading profile picture: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/schedule/<int:schedule_id>/color', methods=['PUT'])
@login_required
def api_update_schedule_color(schedule_id):
    """Update only the color of a schedule item - accessible by both students and teachers"""
    print(f"[COLOR UPDATE] Received request for schedule_id: {schedule_id}")
    print(f"[COLOR UPDATE] Current user: {current_user.username if current_user.is_authenticated else 'Not logged in'}")
    
    data = request.get_json()
    new_color = data.get('color')
    print(f"[COLOR UPDATE] New color: {new_color}")
    
    if not new_color:
        print("[COLOR UPDATE] Error: No color provided")
        return jsonify({'success': False, 'error': 'Color is required'}), 400
    
    conn = db.get_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE schedule 
            SET color = %s 
            WHERE id = %s
        """, (new_color, schedule_id))
        
        conn.commit()
        print(f"[COLOR UPDATE] Successfully updated schedule {schedule_id} to color {new_color}")
        
        cursor.close()
        conn.close()
        
        # ⚡ Real-time update: notify all clients
        try:
            socketio.emit('schedule_updated', {'action': 'color_change'}, namespace='/')
            print("[COLOR UPDATE] WebSocket event sent")
        except Exception as ws_error:
            print(f"[COLOR UPDATE] WebSocket error (non-critical): {ws_error}")
        
        return jsonify({'success': True, 'message': 'Color updated successfully'})
    except Exception as e:
        print(f"[COLOR UPDATE] Error updating color: {e}")
        print(f"[COLOR UPDATE] Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Try to close connection if it's still open
        try:
            if conn:
                conn.close()
        except:
            pass
        
        return jsonify({'success': False, 'error': str(e)}), 500

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
    )
    if result:
        return jsonify({'success': True, 'message': 'Teacher added'})
    return jsonify({'success': False, 'error': 'Failed to add teacher'}), 400

@app.route('/api/admin/teachers/<int:teacher_id>', methods=['DELETE', 'PUT'])
@role_required('teacher')
def api_manage_teacher(teacher_id):
    if request.method == 'DELETE':
        result = db.delete_teacher(teacher_id)
        if result:
            return jsonify({'success': True, 'message': 'Teacher deleted'})
        return jsonify({'success': False, 'error': 'Failed to delete'}), 400
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        try:
            client = db.get_supabase_client()
            username = data.get('username')
            
            # Check username conflict
            if username:
                existing = client.table('teachers').select('id').eq('username', username).neq('id', teacher_id).execute()
                if existing.data:
                    return jsonify({'success': False, 'error': 'Username already taken'}), 400
            
            # Prepare update data
            update_data = {
                'username': username,
                'name': data['name'],
                'subject': data.get('subject'),
                'contact': data.get('contact'),
                'room': data.get('room')
            }
            
            # Store password as plain text (SECURITY WARNING: Not recommended!)
            if data.get('password'):
                update_data['password'] = data['password']
            
            # Update
            client.table('teachers').update(update_data).eq('id', teacher_id).execute()
            
            return jsonify({'success': True, 'message': 'Teacher updated'})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/students', methods=['POST'])
@role_required('teacher')
def api_add_student():
    data = request.get_json()
    result = db.add_student(
        data['username'],
        data['password'],
        data['name']
    )
    if result:
        return jsonify({'success': True, 'message': 'Student added'})
    return jsonify({'success': False, 'error': 'Failed to add student'}), 400

@app.route('/api/admin/students/<int:student_id>', methods=['DELETE', 'PUT'])
@role_required('teacher')
def api_manage_student(student_id):
    if request.method == 'DELETE':
        result = db.delete_student(student_id)
        if result:
            return jsonify({'success': True, 'message': 'Student deleted'})
        return jsonify({'success': False, 'error': 'Failed to delete'}), 400
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        try:
            client = db.get_supabase_client()
            username = data.get('username')
            
            # Check username conflict
            if username:
                existing = client.table('students').select('id').eq('username', username).neq('id', student_id).execute()
                if existing.data:
                    return jsonify({'success': False, 'error': 'Username already taken'}), 400
            
            # Prepare update data
            update_data = {
                'username': username,
                'name': data['name']
            }
            
            # Store password as plain text (SECURITY WARNING: Not recommended!)
            if data.get('password'):
                update_data['password'] = data['password']
            
            # Update
            client.table('students').update(update_data).eq('id', student_id).execute()
            
            return jsonify({'success': True, 'message': 'Student updated'})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

# QR Code Routes
@app.route('/qrcode')
def qrcode_page():
    """Display QR code page for sharing the website"""
    return send_from_directory('static', 'qrcode.html')

@app.route('/api/qrcode-image')
def generate_qrcode():
    """Generate QR code image for the current public URL"""
    # Use the current request URL hostname
    url = request.host_url
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/api/public-url')
def get_public_url():
    """Return the current public URL"""
    return jsonify({
        'url': request.host_url,
        'has_ngrok': False
    })

# Teacher Profile
@app.route('/api/profile', methods=['GET', 'PUT'])
@role_required('teacher')
def api_teacher_profile():
    user = current_user
    
    if request.method == 'GET':
        teacher = db_helpers.get_teacher_by_id(int(user.id.split(':')[1]))
        if teacher:
            return jsonify(teacher)
        return jsonify({'success': False, 'error': 'Teacher not found'}), 404
    
    elif request.method == 'PUT':
        teacher_id = int(user.id.split(':')[1])
        
        # Handle file upload if present - Upload to Supabase Storage
        profile_picture_url = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                # Validate file type
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    try:
                        import uuid
                        ext = file.filename.rsplit('.', 1)[1].lower()
                        filename = f"teacher_{teacher_id}_{uuid.uuid4().hex}.{ext}"
                        
                        # Read file content
                        file_content = file.read()
                        
                        # Upload to Supabase Storage
                        client = db.get_supabase_client()
                        storage_response = client.storage.from_('profile-pictures').upload(
                            path=filename,
                            file=file_content,
                            file_options={"content-type": file.content_type, "upsert": "true"}
                        )
                        
                        # Get public URL
                        profile_picture_url = client.storage.from_('profile-pictures').get_public_url(filename)
                        print(f"✅ Uploaded profile picture to Supabase Storage: {profile_picture_url}")
                        
                    except Exception as e:
                        print(f"❌ Error uploading to Supabase Storage: {e}")
        
        # Get form data
        username = request.form.get('username')
        name = request.form.get('name')
        subject = request.form.get('subject')
        contact = request.form.get('contact')
        room = request.form.get('room')
        
        # Update basic profile
        result = db.update_teacher_profile(
            teacher_id,
            username,
            name,
            subject,
            contact,
            room
        )
        
        # Update profile picture URL in database if uploaded
        if result and profile_picture_url:
            try:
                client = db.get_supabase_client()
                client.table('teachers').update({
                    'profile_picture': profile_picture_url
                }).eq('id', teacher_id).execute()
                print(f"✅ Updated profile_picture in database: {profile_picture_url}")
            except Exception as e:
                print(f"❌ Error updating profile picture in database: {e}")


        
        if result:
            return jsonify({
                'success': True, 
                'message': 'Profile updated',
                'username': username
            })
        return jsonify({'success': False, 'error': 'Failed to update profile or username already taken'}), 400

if __name__ == '__main__':
    print("=== TeachMap PWA Server Starting ===")
    
    # Initialize database
    print("Initializing database connection...")
    if db.init_database():
        print("Database initialized successfully")
    else:
        print("Warning: Database initialization failed")
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print(f"\n[SUCCESS] Server is running!")
    print(f"Local access: http://localhost:{port}")
    print(f"Network access: http://<your-ip>:{port}")
    print("Real-time WebSocket enabled!\n")
    
    # Use socketio.run for development, gunicorn for production
    if app.config['DEBUG']:
        socketio.run(app, debug=True, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
    else:
        socketio.run(app, debug=False, host='0.0.0.0', port=port)
