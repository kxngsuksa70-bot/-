# TeachMap PWA

A Progressive Web Application for managing teacher schedules and student dashboards with real-time updates.

## 🚀 Features

- **Teacher Dashboard**: Manage teaching schedules, profile, and availability
- **Student Dashboard**: View all teacher schedules and classrooms
- **Real-time Updates**: WebSocket-powered live schedule synchronization
- **Schedule Management**: Add, edit, delete, and color-code schedules
- **User Management**: Admin panel for managing teachers and students
- **Profile Pictures**: Upload and manage profile photos
- **QR Code Sharing**: Generate QR codes for easy mobile access
- **PWA Support**: Installable on mobile devices with offline capability

## 🛠️ Technology Stack

**Backend:**
- Flask 3.0.0 (Python web framework)
- Flask-SocketIO (Real-time WebSocket)
- PostgreSQL (Supabase database)
- psyc opg2 (PostgreSQL adapter)
- Flask-Bcrypt (Password hashing)

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Service Worker for PWA
- SocketIO Client for real-time updates

**Deployment:**
- Railway.app (recommended)
- Supabase PostgreSQL database

---

## 📋 Prerequisites

### For Local Development:
- Python 3.8+
- Git
- Supabase account (free tier available)

### For Deployment:
- GitHub account
- Railway.app account (free $5 monthly credit)
- Supabase account

---

## 🔧 Quick Start (Local Development)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd puyfai
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
cd web
pip install -r requirements.txt
```

### 4. Setup Supabase Database

1. Go to [Supabase](https://supabase.com) and create a new project
2. Go to **SQL Editor** in your Supabase dashboard
3. Copy and paste the contents of `supabase_schema.sql`
4. Run the SQL script to create tables and sample data
5. Get your database credentials from **Settings → Database**

### 5. Configure Environment Variables
```bash
# Create .env file in the root directory
cp .env.example .env

# Edit .env and add your Supabase credentials
```

Example `.env` file:
```env
SUPABASE_HOST=db.abcdefghijk.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_password_here

SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 6. Run the Application
```bash
python web/app.py
```

Visit `http://localhost:5000` in your browser.

---

## 🚀 Deployment to Railway.app

### Step 1: Prepare GitHub Repository

1. **Initialize Git** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit - Ready for deployment"
```

2. **Create GitHub Repository**:
   - Go to [GitHub](https://github.com) and create a new repository
   - Follow the instructions to push your code:
```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### Step 2: Setup on Railway

1. **Sign up** at [Railway.app](https://railway.app)
2. Click "**New Project**"
3. Select "**Deploy from GitHub repo**"
4. Choose your `puyfai` repository
5. Railway will automatically detect it's a Python app

### Step 3: Configure Environment Variables

In Railway dashboard:
1. Go to your project → **Variables** tab
2. Add the following variables:

```
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_supabase_password
SECRET_KEY=generate_random_32_character_key
DEBUG=False
PORT=5000
```

**To generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Deploy!

1. Railway will automatically deploy when you push to GitHub
2. Wait for build to complete (2-3 minutes)
3. Click "**Generate Domain**" to get your public URL
4. Visit your URL - your app is live! 🎉

---

## 👤 Default Login Credentials

**Teacher:**
- Username: `teacher1`
- Password: `1234`

**Student:**
- Username: `student1`
- Password: `1234`

⚠️ **Change these in production!**

---

## 📁 Project Structure

```
puyfai/
├── web/                    # Main web application
│   ├── app.py             # Flask application
│   ├── requirements.txt   # Python dependencies
│   └── static/            # Frontend files
│       ├── html files
│       ├── css/
│       ├── js/
│       └── images/
├── database_postgres.py   # PostgreSQL database layer
├── database_pwa_helpers.py
├── supabase_schema.sql    # Database schema
├── Procfile              # Railway start command
├── railway.toml          # Railway configuration
├── .env.example          # Environment template
├── .gitignore
└── README.md
```

---

## 🔒 Security Notes

### Implemented:
- ✅ Environment variables for sensitive data
- ✅ CORS configuration
- ✅ Production/development mode switching
- ✅ PostgreSQL connection pooling

### TODO (For Production):
- ⚠️ Implement bcrypt password hashing (currently plain text)
- ⚠️ Add rate limiting for API endpoints
- ⚠️ Enable HTTPS only in production
- ⚠️ Add input validation and sanitization

---

## 🐛 Troubleshooting

### Database Connection Failed
- Check Supabase credentials in `.env`
- Verify Supabase project is running
- Check if IP is allowed in Supabase settings

### WebSocket Not Working
- Ensure `eventlet` is installed
- Check CORS settings
- Verify Railway has WebSocket support enabled

### Railway Deploy Failed
- Check build logs in Railway dashboard
- Verify `Procfile` exists
- Ensure all dependencies in `requirements.txt`

---

## 📝 API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/logout` - User logout

### Schedules
- `GET /api/schedule` - Get teacher schedule
- `POST /api/schedule` - Add schedule
- `PUT /api/schedule/<id>` - Update schedule
- `DELETE /api/schedule/<id>` - Delete schedule

### Public
- `GET /api/teachers` - List all teachers
- `GET /api/all-schedules` - Get all schedules

[See full API documentation](web/admin_edit_endpoints.txt)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 💡 Support

For issues and questions:
1. Check [Supabase Documentation](https://supabase.com/docs)
2. Check [Railway Documentation](https://docs.railway.app)
3. Open an issue on GitHub

---

## 🙏 Acknowledgments

- Flask framework
- Supabase for PostgreSQL hosting
- Railway.app for deployment platform
- Socket.IO for real-time functionality
