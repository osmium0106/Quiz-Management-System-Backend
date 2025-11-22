# 🚀 Deployment Guide - Free Platforms

## 🏆 Recommended: Railway (Best for Your Project)

### Why Railway?
- ✅ **Perfect Docker Support**: Your existing Dockerfile works as-is
- ✅ **PostgreSQL Included**: Free PostgreSQL database
- ✅ **GitHub Integration**: Auto-deploy on push
- ✅ **Environment Variables**: Easy config management
- ✅ **$5/month Credit**: Usually covers small to medium apps
- ✅ **Custom Domains**: Free SSL certificates

### 🚀 Deploy to Railway (5 Minutes Setup):

#### Step 1: Install Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Or download from: https://railway.app/cli
```

#### Step 2: Login and Deploy
```bash
# Login to Railway
railway login

# Navigate to your project
cd Quiz-Management-System-Backend

# Initialize Railway project
railway init

# Link to your GitHub repo (optional but recommended)
railway link

# Add PostgreSQL database
railway add postgresql

# Deploy your app
railway up
```

#### Step 3: Set Environment Variables
In Railway dashboard, add these variables:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,localhost
DATABASE_URL=postgresql://user:pass@host:port/dbname  # Auto-provided by Railway
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

#### Step 4: Access Your API
- **API URL**: `https://your-app-name.railway.app/api/v1/`
- **Swagger**: `https://your-app-name.railway.app/swagger/`
- **Admin**: `https://your-app-name.railway.app/admin/`

---

## 🥈 Alternative: Render (Completely Free)

### Why Render?
- ✅ **100% Free**: No credit card required
- ✅ **Docker Support**: Your Dockerfile works
- ✅ **Free PostgreSQL**: 1GB database included
- ⚠️ **Limitation**: Apps sleep after 15min inactivity

### 🚀 Deploy to Render:

#### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Connect your repository

#### Step 2: Create PostgreSQL Database
1. Click "New" → "PostgreSQL"
2. Choose free plan
3. Note the connection details

#### Step 3: Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repo
3. Use these settings:
   - **Environment**: Docker
   - **Build Command**: (leave empty)
   - **Start Command**: (leave empty - uses Dockerfile)

#### Step 4: Environment Variables
Add in Render dashboard:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname  # From Step 2
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

---

## 🥉 Alternative: Fly.io

### 🚀 Deploy to Fly.io:

#### Step 1: Install Fly CLI
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Or on Windows:
iwr https://fly.io/install.ps1 -useb | iex
```

#### Step 2: Deploy
```bash
# Login
flyctl auth login

# Launch app (from your project directory)
flyctl launch

# Add PostgreSQL
flyctl postgres create

# Deploy
flyctl deploy
```

---

## 📋 Pre-Deployment Checklist

### ✅ Your Project is Already Ready!
- ✅ **Dockerfile**: Production-ready
- ✅ **Environment Variables**: Configured in .env
- ✅ **Database**: PostgreSQL support
- ✅ **Static Files**: Configured
- ✅ **CORS**: Ready for frontend
- ✅ **Railway Config**: Added (railway.toml)

### 🔧 Quick Updates Needed:

#### 1. Update ALLOWED_HOSTS for Production
```python
# In settings.py, you'll need to add your deployment domain
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'your-app-name.railway.app',  # Add your Railway domain
    # or 'your-app-name.onrender.com' for Render
]
```

#### 2. Update CORS for Production Frontend
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.com",  # Add your frontend domain
]
```

---

## 🎯 My Recommendation: **Railway**

**Why Railway is Perfect for You:**
1. **Zero Configuration**: Your Docker setup works immediately
2. **PostgreSQL Included**: No separate database setup
3. **GitHub Integration**: Auto-deploys when you push code
4. **Professional**: Custom domains, SSL, environment management
5. **Cost Effective**: $5 credit usually lasts months for development

**Deployment Time**: ~5 minutes
**Maintenance**: Zero - just push to GitHub

### 🚀 Ready to Deploy?
1. Install Railway CLI: `npm install -g @railway/cli`
2. Run: `railway login`
3. Run: `railway init` in your project
4. Run: `railway up`
5. Your API is live! 🎉

---

## 💡 Pro Tips:

### For Railway:
- Use environment variables for all sensitive data
- Enable GitHub integration for auto-deployments
- Monitor usage in Railway dashboard

### For Render (Free):
- Expect 30-second cold starts after inactivity
- Use a service like UptimeRobot to ping your API and keep it awake
- Upgrade to paid plan ($7/month) to eliminate sleeping

### For All Platforms:
- Always use HTTPS in production
- Set up proper monitoring
- Keep your dependencies updated

Choose **Railway** for the best experience with your Django + Docker + PostgreSQL setup! 🚀