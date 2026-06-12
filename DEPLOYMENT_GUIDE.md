# LivestockGuard Deployment Guide

## Overview
This guide covers deploying the LivestockGuard application stack:
- **Backend**: FastAPI application on Render
- **Database**: PostgreSQL on Neon
- **Frontend**: Flutter mobile app
- **Notifications**: Firebase Cloud Messaging (FCM)

---

## Part 1: Prerequisites

### Required Tools & Accounts
- [ ] Neon account (https://neon.tech)
- [ ] Render account (https://render.com)
- [ ] Firebase project (https://firebase.google.com/console)
- [ ] GitHub account (for connecting Render)
- [ ] Git CLI installed
- [ ] Flutter SDK (for mobile app)

### Repository Setup
1. Push your code to GitHub:
   ```bash
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

---

## Part 2: Neon Database Setup

### Step 1: Create Neon Project
1. Go to https://neon.tech and sign in
2. Click **"Create a project"**
3. Configure:
   - **Project name**: `livestockguard`
   - **Database name**: `livestockguard`
   - **Region**: Select region closest to your users
   - **PostgreSQL version**: Latest available
4. Click **"Create project"**

### Step 2: Get Connection String
1. In Neon dashboard, go to your project
2. Click **"Connection string"** or **"Connection details"**
3. Select **"Connection pooler"** (recommended for serverless apps)
4. Copy the connection string that looks like:
   ```
   postgresql://user:password@ep-xxx.region.databases.neon.tech/livestockguard?sslmode=require
   ```
5. **Save this** - you'll need it for environment variables

### Step 3: Initialize Database Schema
1. Go to Neon dashboard → **"SQL Editor"**
2. Paste the contents of `backend/db_schema.sql`
3. Run all SQL commands
4. Verify tables are created by running:
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```

### Step 4: Create Neon API Key (for automated backups)
1. Go to **Account settings** → **API keys**
2. Click **"Create API key"**
3. Name it: `livestockguard-deployment`
4. Save the key (you won't see it again)

---

## Part 3: Firebase Setup

### Step 1: Create Firebase Project
1. Go to https://firebase.google.com/console
2. Click **"Create a project"**
3. Name: `livestockguard`
4. Follow setup wizard
5. Enable Google Analytics (optional)

### Step 2: Generate Service Account Key
1. In Firebase console, go to **Project settings** → **Service accounts**
2. Click **"Generate new private key"**
3. Save as JSON file
4. **Important**: This will be used for backend push notifications

### Step 3: Configure Firebase for Flutter App
1. In Firebase console, click **"Add app"** → **Flutter**
2. Download `google-services.json` and `GoogleService-Info.plist`
3. Follow Firebase Flutter setup instructions

### Step 4: Enable Firestore (optional, for future features)
1. In Firebase console, go to **"Firestore Database"**
2. Click **"Create database"**
3. Select region, production mode
4. Create collection structure as needed

---

## Part 4: Render Backend Setup

### Step 1: Create Render Service
1. Go to https://render.com and sign in
2. Click **"New"** → **"Web Service"**
3. **Connect your GitHub repository** (authorize Render with GitHub)
4. Select the `livestockguard` repository
5. Configure:
   - **Name**: `livestockguard-backend`
   - **Region**: Same as Neon region
   - **Branch**: `main`
   - **Runtime**: Python 3.11
   - **Build command**: 
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start command**:
     ```bash
     cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
     ```

### Step 2: Add Environment Variables
1. In Render service dashboard, go to **"Environment"**
2. Add the following variables:

#### Critical Variables (MUST SET)
```
DATABASE_URL=postgresql+psycopg://user:password@ep-xxx.region.databases.neon.tech/livestockguard?sslmode=require
JWT_SECRET=<generate-strong-random-string>
```

#### Optional Variables (Defaults Provided)
```
BACKEND_HOST=0.0.0.0
BACKEND_PORT=10000
FIREBASE_CREDENTIALS_PATH=/opt/render/project/src/backend/firebase/serviceAccountKey.json
```

### Step 3: Configure Secret Files
Render requires special handling for the Firebase credentials JSON file:

**Option A: Using Render's Secret Files**
1. In Render dashboard, go to **"Environment"**
2. Scroll to **"Secret files"**
3. Click **"Add secret file"**
4. **Filename**: `firebase/serviceAccountKey.json`
5. **Contents**: Paste the entire Firebase service account JSON
6. Click **"Save"**

**Option B: Commit Encrypted (Recommended)**
1. Add `backend/firebase/serviceAccountKey.json` to `.gitignore` if not already
2. Encrypt using git-crypt or similar before committing
3. Or manually create the file in Render's dashboard (Option A)

### Step 4: Configure Build Settings
1. Go to **"Settings"** → **"Build & Deploy"**
2. Set **"Build filter"**:
   ```
   backend/**
   ```
   (Only rebuild when backend changes)
3. Enable **"Auto-Deploy"** for main branch

### Step 5: Deploy
1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Watch deployment logs for errors
3. Once deployed, note your service URL: `https://livestockguard-backend.onrender.com`

### Step 6: Verify Deployment
```bash
curl https://livestockguard-backend.onrender.com/
# Should return: "LivestockGuard backend running"
```

---

## Part 5: Environment Variables Reference

### Backend (.env file for local development)
```env
# Database
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/livestockguard

# API Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Security
JWT_SECRET=your-super-secret-key-at-least-32-characters-long

# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase/serviceAccountKey.json
```

### Required Secrets for Render
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Strong random string (generate with: `openssl rand -hex 32`)
- `firebase/serviceAccountKey.json` - Uploaded as secret file

### How to Generate JWT_SECRET
```bash
# On macOS/Linux
openssl rand -hex 32

# On Windows (PowerShell)
[System.BitConverter]::ToString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)).Replace("-","").ToLower()
```

---

## Part 6: Manual Steps Required Before Deployment

### Step 1: Prepare Firebase Credentials
```bash
# Download service account JSON from Firebase console
# Save to: backend/firebase/serviceAccountKey.json
# This file should NOT be committed to version control
echo "firebase/serviceAccountKey.json" >> backend/.gitignore
```

### Step 2: Generate Strong Secrets
```bash
# Generate JWT_SECRET
JWT_SECRET=$(openssl rand -hex 32)
echo "JWT_SECRET=$JWT_SECRET"

# Save for later use in Render environment
```

### Step 3: Test Database Connection Locally (Optional)
```bash
cd backend

# Create .env file with Neon connection string
echo "DATABASE_URL=postgresql+psycopg://user:password@ep-xxx.region.databases.neon.tech/livestockguard?sslmode=require" > .env
echo "JWT_SECRET=$(openssl rand -hex 32)" >> .env

# Install dependencies
pip install -r requirements.txt

# Run database initialization
python -c "from app.db.init_db import init_database; init_database()"

# Should output: "Database tables initialized" or similar
```

### Step 4: Configure CORS for Mobile App
In `backend/app/main.py`, update CORS if needed:
```python
# For production, replace ["*"] with your specific domains
allow_origins=[
    "http://localhost:3000",  # Local dev
    "https://your-frontend-domain.com",  # Production
]
```

### Step 5: Model Files Setup
Ensure ML model files exist:
- `backend/model_5classes.pth` - PyTorch model
- `backend/livestock_symptoms_dataset.csv` - Training data
- `backend/symptom_disease_matrix.csv` - Disease-symptom mappings

These should be committed to the repo (or uploaded separately if too large).

### Step 6: Reports Directory
Create reports directory if not exists:
```bash
mkdir -p backend/reports
chmod 755 backend/reports
```

---

## Part 7: Flutter App Configuration

### Step 1: Update API Endpoint
In `livestock/lib/src/config/api_config.dart` or similar:
```dart
const String API_BASE_URL = 'https://livestockguard-backend.onrender.com';
```

### Step 2: Firebase Configuration
1. Place `google-services.json` in `livestock/android/app/`
2. Place `GoogleService-Info.plist` in `livestock/ios/Runner/`

### Step 3: Build and Release APK
```bash
cd livestock

# Get dependencies
flutter pub get

# Build APK
flutter build apk --release

# Build iOS (requires macOS)
flutter build ios --release
```

### Step 4: Configure Push Notifications
Ensure FCM tokens are sent to backend:
```dart
// In your Flutter app initialization
final fcmToken = await FirebaseMessaging.instance.getToken();
// Send this token to backend via API call
```

---

## Part 8: Manual Commands to Run

### After Render Deployment (One-time Setup)

```bash
# 1. SSH into Render or run via Render Shell
# (Navigate to your service in Render dashboard → "Shell")

# 2. Run database migrations (if any)
cd backend
python -c "from app.db.init_db import init_database; init_database()"

# 3. Verify database connection
python -c "from app.db.session import SessionLocal; db = SessionLocal(); print(db.execute('SELECT 1').scalar())"

# 4. Seed initial disease/symptom data
python -c "
from app.db.init_db import seed_from_matrix_if_needed
from app.db.session import SessionLocal
from pathlib import Path
db = SessionLocal()
seed_from_matrix_if_needed(Path('/opt/render/project/src/backend'), db)
print('Seeding complete')
"
```

### Monitoring & Logs

```bash
# View Render logs (in dashboard)
# Go to: Service → Logs

# Monitor database (Neon)
# Go to: Neon Dashboard → Monitoring

# Test API endpoints
curl -X GET https://livestockguard-backend.onrender.com/
curl -X POST https://livestockguard-backend.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "full_name": "Test User"}'
```

---

## Part 9: Secrets Checklist

### Create These Before Deploying:

| Secret | Where to Get | Where It Goes | Example |
|--------|-------------|---------------|---------|
| `DATABASE_URL` | Neon Dashboard → Connection | Render Env Var | `postgresql+psycopg://user:pass@ep-xxx.neon.tech/livestockguard?sslmode=require` |
| `JWT_SECRET` | Generate with `openssl rand -hex 32` | Render Env Var | `a3f8d2e9c4b1f6a7e9d2c3b4f5a6e7d8...` |
| `serviceAccountKey.json` | Firebase Console → Service Accounts | Render Secret File | JSON with private_key, client_id, etc. |
| `google-services.json` | Firebase Console → Add App (Flutter) | `livestock/android/app/` | JSON for Android |
| `GoogleService-Info.plist` | Firebase Console → Add App (Flutter) | `livestock/ios/Runner/` | PLIST for iOS |

---

## Part 10: Post-Deployment Testing

### Health Check
```bash
# 1. API is running
curl https://livestockguard-backend.onrender.com/

# 2. Database is connected
curl https://livestockguard-backend.onrender.com/catalog/diseases

# 3. Authentication works
curl -X POST https://livestockguard-backend.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "deploy-test@example.com",
    "password": "TestPassword123!",
    "full_name": "Deploy Test"
  }'

# 4. Detection endpoint works (requires image upload)
curl -X POST https://livestockguard-backend.onrender.com/detection/predict \
  -F "file=@test-image.jpg"
```

### Flutter App Testing
1. Update API endpoint to production URL
2. Rebuild and test authentication flow
3. Test disease detection feature
4. Verify push notifications

---

## Part 11: Troubleshooting

### Database Connection Issues
**Error**: `ERROR: could not connect to server`

**Solution**:
1. Verify DATABASE_URL format in Render environment
2. Check Neon connection pooler is enabled
3. Test locally with `psql` command:
   ```bash
   psql "postgresql://user:pass@ep-xxx.neon.tech/livestockguard?sslmode=require"
   ```

### Firebase Credentials Not Found
**Error**: `Firebase credentials not found`

**Solution**:
1. Upload `serviceAccountKey.json` as Render secret file
2. Or mount file using `.env` file on Render
3. Check path in `FIREBASE_CREDENTIALS_PATH` environment variable

### Model Loading Fails
**Error**: `FileNotFoundError: model_5classes.pth`

**Solution**:
1. Ensure model file is committed to GitHub
2. Check `backend/` directory structure matches local
3. Verify file size < Render's limits (512MB max)

### SSL/TLS Certificate Issues
**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**:
- Use `?sslmode=require` in DATABASE_URL
- Neon automatically provides valid certificates

---

## Part 12: Maintenance & Monitoring

### Regular Tasks
- [ ] Monitor Neon database storage usage
- [ ] Check Render service health (uptime, CPU, memory)
- [ ] Review API error logs weekly
- [ ] Backup database (Neon has automatic backups)
- [ ] Update dependencies monthly

### Neon Maintenance
```bash
# Check connection limit usage
SELECT count(*) FROM pg_stat_activity;

# View slow queries
SELECT query, mean_exec_time FROM pg_stat_statements 
ORDER BY mean_exec_time DESC LIMIT 10;
```

### Render Maintenance
1. Enable automatic deployments for production readiness
2. Set up alerts for high memory/CPU usage
3. Configure auto-restart on failure

---