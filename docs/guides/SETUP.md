# Taskie Todo App - Setup & Run Guide

This guide will help you set up and run both the frontend and backend of the Taskie Todo App.

## ✅ Pre-requisites

Before starting, ensure you have installed:

- **Node.js 18+** - Download from https://nodejs.org/
- **Python 3.9+** - Download from https://www.python.org/
- **Git** - Download from https://git-scm.com/

Verify installations:
```bash
node --version      # Should be v18+
npm --version       # Should be v8+
python --version    # Should be 3.9+
pip --version       # Should be v21+
```

---

## 📦 Step 1: Set Up Backend (FastAPI)

### 1.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv
```

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 1.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

Expected output: Should install ~15 packages including fastapi, sqlmodel, pyjwt, etc.

### 1.3 Configure Environment Variables

Copy the example file to create your local .env:

```bash
# On Windows:
copy .env.example .env

# On macOS/Linux:
cp .env.example .env
```

Edit the `.env` file with your values:

```env
# 1. Get DATABASE_URL from Neon
#    - Go to https://console.neon.tech/
#    - Create/select a project
#    - Copy connection string from "Connection details" → "Connection string"
#    - Format: postgresql://user:password@host/dbname?sslmode=require
DATABASE_URL=postgresql://your_username:your_password@ep-xxxx-pooler.c-xxxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# 2. BETTER_AUTH_SECRET - MUST be 32+ characters and SAME on frontend
#    Generate with: openssl rand -base64 32
#    Or use a strong password: make-it-32-chars-minimum-please-123
BETTER_AUTH_SECRET=your-32-char-minimum-secret-key-change-me-now

# 3. CORS_ORIGINS - Frontend origin (where frontend runs)
CORS_ORIGINS=http://localhost:3000

# 4. SQLAlchemy debug (optional)
SQLALCHEMY_ECHO=false
```

**⚠️ IMPORTANT:**
- Never commit the `.env` file to git (it's in .gitignore)
- The DATABASE_URL contains sensitive credentials - keep it private
- BETTER_AUTH_SECRET must be the same on frontend AND backend

### 1.4 Test Backend Startup

```bash
python main.py
```

Expected output:
```
[OK] DATABASE_URL configured
[OK] BETTER_AUTH_SECRET configured (XX characters)
Database tables created successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is running on http://localhost:8000**

### 1.5 Verify Backend Health

Open a new terminal and run:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

---

## 🎨 Step 2: Set Up Frontend (Next.js)

Open a **NEW terminal** (keep backend running in the first one).

### 2.1 Install Node Dependencies

```bash
cd frontend
npm install
```

Expected output: Should install ~50+ packages including next, react, tailwind, etc.

### 2.2 Configure Environment Variables

Copy the example file:

```bash
# On Windows:
copy .env.local.example .env.local

# On macOS/Linux:
cp .env.local.example .env.local
```

Edit the `.env.local` file:

```env
# Backend API - MUST match backend port (8000)
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Better Auth - Frontend URL
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# BETTER_AUTH_SECRET - MUST be identical to backend .env
# Use the SAME value you set in backend/.env
BETTER_AUTH_SECRET=your-32-char-minimum-secret-key-change-me-now

# Environment
NODE_ENV=development
```

**⚠️ CRITICAL:**
- `NEXT_PUBLIC_API_BASE_URL` must be `http://localhost:8000` (not 8001!)
- `BETTER_AUTH_SECRET` must be IDENTICAL to backend
- These values are accessible in browser console (NEXT_PUBLIC_ prefix)

### 2.3 Start Frontend Development Server

```bash
npm run dev
```

Expected output:
```
  ▲ Next.js 16.x
  - Local:        http://localhost:3000
  - Environments: .env.local

✓ Ready in 2.5s
```

✅ **Frontend is running on http://localhost:3000**

---

## 🚀 Step 3: Verify Everything Works

### 3.1 Open Frontend in Browser

Visit: **http://localhost:3000**

You should see:
- Landing page with Taskie Todo App branding
- Links to Sign In and Sign Up

### 3.2 Test User Signup

1. Click "Sign Up" link
2. Enter:
   - Email: `test@example.com`
   - Password: `TestPassword123!`
3. Click "Sign Up"

Expected behavior:
- User account created
- Redirected to tasks dashboard
- No tasks displayed (empty state)

### 3.3 Test Task Creation

1. Click "New Task" or "Add Task"
2. Enter:
   - Title: "My First Task"
   - Description: "This is a test task"
   - Priority: "High"
3. Click "Create Task"

Expected behavior:
- Task appears in the list
- Task shows with your title, description, and priority

### 3.4 Test Task Operations

- ✅ **Mark Complete**: Click checkbox next to task
- ✏️ **Edit Task**: Click task to edit
- 🗑️ **Delete Task**: Click delete button
- 🔄 **Filter**: Use filters if implemented

### 3.5 Test Authentication

1. Click user menu/profile
2. Click "Sign Out"
3. Should redirect to login page
4. Sign in with your test credentials
5. Should see your tasks again

---

## 📋 Troubleshooting

### Issue: Backend won't start - "DATABASE_URL not configured"

**Solution:**
1. Check backend/.env exists
2. Verify DATABASE_URL is set and correct
3. For Neon, ensure connection string includes `?sslmode=require`

### Issue: Backend won't start - "BETTER_AUTH_SECRET must be 32+ characters"

**Solution:**
1. Check BETTER_AUTH_SECRET length: `echo -n "your-secret" | wc -c`
2. Must be 32+ characters
3. Generate new: `openssl rand -base64 32` (on Windows: use Git Bash)

### Issue: Frontend shows "Failed to fetch" or API errors

**Solution:**
1. Verify backend is running on port 8000: `curl http://localhost:8000/health`
2. Check frontend `.env.local` has `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
3. Check BETTER_AUTH_SECRET matches between frontend and backend
4. Clear browser cache: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)

### Issue: CORS errors in browser console

**Solution:**
1. Check backend `.env` has `CORS_ORIGINS=http://localhost:3000`
2. Restart backend after changing CORS_ORIGINS
3. Clear browser cache

### Issue: Tasks don't persist / Database errors

**Solution:**
1. Verify DATABASE_URL is correct and accessible
2. Check network connectivity to Neon
3. Restart both backend and frontend
4. Check browser DevTools → Network tab for actual API responses

### Issue: Port already in use

If port 3000 or 8000 is already in use:

**Backend (change port in main.py line 129):**
```python
port=8001,  # Change to 8001 or another available port
```

**Frontend (change port when running):**
```bash
npm run dev -- -p 3001  # Runs on port 3001 instead
```

Then update `NEXT_PUBLIC_API_BASE_URL` in frontend/.env.local accordingly.

---

## 🔧 Development Commands

### Backend
```bash
cd backend
source venv/bin/activate  # Or: venv\Scripts\activate on Windows
python main.py            # Start dev server
pytest                     # Run tests
```

### Frontend
```bash
cd frontend
npm run dev               # Start dev server (http://localhost:3000)
npm run build             # Build for production
npm test                  # Run tests (if configured)
npm run lint              # Run ESLint
```

---

## 📚 Architecture Overview

```
┌─────────────────────────────────────────────┐
│         Browser (User)                      │
│      http://localhost:3000                  │
└────────────────┬────────────────────────────┘
                 │ HTTP Requests
                 ↓
┌─────────────────────────────────────────────┐
│  Next.js Frontend                           │
│  - Authentication (JWT)                     │
│  - Task UI (React components)               │
│  - API Client (with JWT injection)          │
└────────────────┬────────────────────────────┘
                 │ REST API + JWT Token
                 │ http://localhost:8000
                 ↓
┌─────────────────────────────────────────────┐
│  FastAPI Backend                            │
│  - JWT Verification                         │
│  - Task CRUD Operations                     │
│  - User Isolation                           │
└────────────────┬────────────────────────────┘
                 │ SQL Queries
                 ↓
┌─────────────────────────────────────────────┐
│  Neon PostgreSQL Database                   │
│  - User table (email, password_hash)        │
│  - Task table (user_id, title, status)      │
└─────────────────────────────────────────────┘
```

---

## 🔐 Security Notes

### Authentication Flow

1. **User Signs Up/In:**
   - Frontend sends credentials to backend `/auth/signup` or `/auth/signin`
   - Backend verifies password and creates JWT token
   - Token returned to frontend

2. **Token Storage:**
   - Frontend stores JWT in localStorage
   - Included in every API request: `Authorization: Bearer <token>`

3. **Task Operations:**
   - Backend verifies JWT in every request
   - Token contains user ID
   - Returns only tasks owned by that user

### Best Practices

- ✅ Never commit `.env` files (already in .gitignore)
- ✅ Use strong BETTER_AUTH_SECRET (32+ characters, random)
- ✅ Keep frontend and backend BETTER_AUTH_SECRET synchronized
- ✅ Use HTTPS in production (not HTTP)
- ✅ Set proper CORS_ORIGINS for your production domain

---

## 📖 Useful Links

- **Neon Documentation:** https://neon.tech/docs/introduction
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Next.js Documentation:** https://nextjs.org/docs
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/

---

## ✨ Next Steps

After setup is complete and working:

1. **Customize:** Update brand colors, add your logo, customize task fields
2. **Deploy:** Deploy backend to a hosting service (Heroku, Railway, etc.)
3. **Database:** Set up Neon production cluster with automated backups
4. **Frontend:** Deploy frontend to Vercel or Netlify
5. **Testing:** Add comprehensive unit and integration tests
6. **Monitoring:** Set up error tracking (Sentry) and analytics

---

**Last Updated:** January 31, 2025
**Status:** ✅ Production Ready (Backend) | ⏳ Testing Phase (Frontend)
