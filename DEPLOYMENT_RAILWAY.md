# 🚀 Railway Deployment Guide

Complete step-by-step guide to deploy TeachMap PWA on Railway.app

---

## Prerequisites

- ✅ GitHub account
- ✅ Railway.app account (sign up at https://railway.app)
- ✅ Supabase account with database setup
- ✅ Code pushed to GitHub repository

---

## Part 1: Supabase Setup (5 minutes)

### 1. Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click "**Start your project**"
3. Sign in with GitHub
4. Click "**New Project**"
5. Fill in:
   - Name: `teachmap-pwa`
   - Database Password: (save this!)
   - Region: Choose closest to your users
6. Click "**Create new project**"
7. Wait 2-3 minutes for setup

### 2. Run Database Schema

1. In Supabase dashboard, click "**SQL Editor**" (left sidebar)
2. Click "**New query**"
3. Copy **entire contents** of `supabase_schema.sql` from your project
4. Paste into SQL editor
5. Click "**Run**" (Ctrl+Enter)
6. You should see "Success. No rows returned"

### 3. Get Database Credentials

1. Go to "**Settings**" → "**Database**" (left sidebar)
2. Scroll to "**Connection string**"
3. Click "**URI**" tab
4. Copy the values (you'll need these):
   - Host: `db.xxxxx.supabase.co`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: Your database password

Keep these safe! You'll add them to Railway.

---

## Part 2: Railway Deployment (10 minutes)

### 1. Sign Up for Railway

1. Go to [https://railway.app](https://railway.app)
2. Click "**Login**"
3. Choose "**Login with GitHub**"
4. Authorize Railway to access your repositories

### 2. Create New Project

1. Click "**New Project**"
2. Select "**Deploy from GitHub repo**"
3. If prompted, grant Railway access to your repositories
4. Find and select your `puyfai` repository
5. Railway will automatically start building!

### 3. Wait for Initial Build

- This takes 2-4 minutes
- You'll see build logs in real-time
- Wait until you see "**Deployment Active**"

### 4. Add Environment Variables

This is the **most important step**!

1. In your Railway project, click the "**Variables**" tab
2. Click "**New Variable**"
3. Add these variables **one by one**:

#### Supabase Database Variables:
```
SUPABASE_HOST = db.xxxxx.supabase.co
```
(Your host from Supabase)

```
SUPABASE_PORT = 5432
```

```
SUPABASE_DB = postgres
```

```
SUPABASE_USER = postgres
```

```
SUPABASE_PASSWORD = your_password_here
```
(Your Supabase database password)

#### Application Variables:
```
SECRET_KEY = 
```
**Generate a random key:**
- Open terminal/command prompt
- Run: `python -c "import secrets; print(secrets.token_hex(32))"`
- Copy the output and paste as value

```
DEBUG = False
```

```
PORT = 5000
```

#### Optional CORS:
```
CORS_ORIGINS = *
```

4. Click "**Deploy**" at the top to restart with new variables

### 5. Generate Public URL

1. Go to "**Settings**" tab
2. Scroll to "**Domains**"
3. Click "**Generate Domain**"
4. Railway will give you a URL like: `your-app.up.railway.app`
5. Click the URL to visit your live app! 🎉

---

## Part 3: Verify Deployment

### Test Your App:

1. Visit your Railway URL
2. You should see the login page
3. Try logging in:
   - Username: `teacher1`
   - Password: `1234`
4. Check if schedules load
5. Try adding a new schedule
6. Test real-time updates (open in two browsers)

### If Something Went Wrong:

#### Check Build Logs:
1. Go to "**Deployments**" tab
2. Click latest deployment
3. Read the logs for errors

#### Common Issues:

**Database Connection Error:**
- Double-check all Supabase environment variables
- Make sure `SUPABASE_PASSWORD` is correct
- Verify Supabase project is running

**Module Not Found:**
- Check `requirements.txt` includes all dependencies
- Re-deploy

**Port Error:**
- Make sure `PORT=5000` is set in variables
- Check `Procfile` exists

---

## Part 4: Ongoing Management

### Automatic Deployments:

Railway automatically deploys when you push to GitHub:
```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main
```

Railway will rebuild and deploy automatically!

### View Logs:

1. Go to "**Deployments**" tab
2. Click active deployment
3. See real-time logs

### Custom Domain (Optional):

1. Go to "**Settings**" → "**Domains**"
2. Click "**Custom Domain**"
3. Follow instructions to add your domain

### Monitor Usage:

1. Go to "**Metrics**" tab
2. See CPU, memory, and network usage
3. Free tier: $5 credit/month (usually enough!)

---

## 🎉 Success Checklist

- ✅ Supabase project created
- ✅ Database schema loaded
- ✅ Railway project deployed
- ✅ All environment variables set
- ✅ Public URL generated
- ✅ App loads and login works
- ✅ Database connection successful
- ✅ Real-time updates working

---

## 🆘 Emergency Troubleshooting

### App Won't Start:

1. Check Railway logs for errors
2. Verify all environment variables
3. Make sure `Procfile` exists:
   ```
   web: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT web.app:app
   ```

### Database Errors:

1. Test Supabase connection:
   - Go to Supabase SQL Editor
   - Run: `SELECT * FROM teachers LIMIT 1;`
   - Should return data
2. Verify connection string in Railway variables

### WebSocket Not Working:

1. Make sure `eventlet` is in `requirements.txt`
2. Check `async_mode='eventlet'` in `app.py`
3. Railway supports WebSocket by default

---

## 📞 Getting Help

1. **Railway Discord**: https://discord.gg/railway
2. **Supabase Discord**: https://discord.supabase.com
3. **Documentation**:
   - Railway: https://docs.railway.app
   - Supabase: https://supabase.com/docs

---

## 🎯 Next Steps

After successful deployment:

1. **Change default passwords** in Supabase:
   ```sql
   UPDATE teachers SET password = 'new_hash' WHERE username = 'teacher1';
   ```

2. **Add your own teachers/students** via admin panel

3. **Customize** the app to your needs

4. **Share** the Railway URL with users!

---

## 💰 Cost Estimate

- **Railway**: $5 free credit/month (usually sufficient for small apps)
- **Supabase**: Free tier (500MB database, 1GB file storage)
- **Total**: FREE for most use cases!

If you exceed free tier:
- Railway: ~$5-10/month
- Supabase: Upgrade to Pro ($25/month) only if needed

---

**Congratulations!** 🎊 Your app is now live and accessible from anywhere in the world!
