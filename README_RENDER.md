# 🚀 Render Deployment Guide - PokeKawaii

This guide will help you deploy the PokeKawaii game to [Render](https://render.com/) - a modern cloud platform that offers free hosting for web applications.

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ A [Render account](https://dashboard.render.com/register) (free)
- ✅ A [GitHub account](https://github.com) with your code pushed
- ✅ Your repository: `https://github.com/KiRzEa/Pikachu`

## 🎯 Deployment Options

You have **two deployment methods**:

### Option 1: Using Blueprint (Recommended) ⭐
Deploy both services at once using the `render.yaml` blueprint file.

### Option 2: Manual Deployment
Deploy each service separately through Render Dashboard.

---

## 🚀 Option 1: Blueprint Deployment (Recommended)

The easiest way to deploy - uses the `render.yaml` file to automatically configure both services.

### Step 1: Connect Your Repository

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select repository: **`KiRzEa/Pikachu`**
5. Click **"Connect"**

### Step 2: Review Blueprint

Render will automatically detect the `render.yaml` file and show:

- ✅ **pokekawaii-backend** - Python web service (FastAPI)
- ✅ **pokekawaii-frontend** - Static site (React)

### Step 3: Configure Services

Review the configuration:

**Backend Service:**
- Name: `pokekawaii-backend`
- Region: Singapore (or your choice)
- Plan: Free
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Frontend Service:**
- Name: `pokekawaii-frontend`
- Region: Singapore (match backend region)
- Plan: Free
- Build Command: `npm install && npm run build`
- Publish Directory: `./dist`

### Step 4: Update Environment Variables

**Important:** After blueprint deploys, update the frontend environment variable:

1. Go to **pokekawaii-frontend** service
2. Navigate to **Environment** tab
3. Find `VITE_API_URL` variable
4. Update value to your backend URL:
   ```
   https://pokekawaii-backend.onrender.com/api
   ```
   (Replace `pokekawaii-backend` with your actual backend service name)
5. Click **"Save Changes"**
6. Service will automatically redeploy

### Step 5: Deploy

1. Click **"Apply"** to create services
2. Wait for deployment (5-10 minutes for first deploy)
3. Monitor build logs in real-time

### Step 6: Access Your App

Once deployed:

- **Frontend URL**: `https://pokekawaii-frontend.onrender.com`
- **Backend API**: `https://pokekawaii-backend.onrender.com`
- **API Docs**: `https://pokekawaii-backend.onrender.com/docs`

---

## 🔧 Option 2: Manual Deployment

Deploy each service separately through the Render Dashboard.

### A. Deploy Backend (FastAPI)

#### Step 1: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect to **`KiRzEa/Pikachu`** repository
4. Click **"Connect"**

#### Step 2: Configure Backend

Fill in the following:

- **Name**: `pokekawaii-backend` (or your choice)
- **Region**: Singapore (or closest to your users)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- **Plan**: Free

#### Step 3: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `ENVIRONMENT` | `production` |

#### Step 4: Deploy Backend

1. Click **"Create Web Service"**
2. Wait for deployment (3-5 minutes)
3. **Copy the backend URL** (e.g., `https://pokekawaii-backend.onrender.com`)

### B. Deploy Frontend (React)

#### Step 1: Create Static Site

1. Click **"New +"** → **"Static Site"**
2. Connect to **`KiRzEa/Pikachu`** repository
3. Click **"Connect"**

#### Step 2: Configure Frontend

Fill in the following:

- **Name**: `pokekawaii-frontend` (or your choice)
- **Region**: Singapore (match backend region)
- **Branch**: `main`
- **Root Directory**: `frontend`
- **Build Command**:
  ```bash
  npm install && npm run build
  ```
- **Publish Directory**: `dist`

#### Step 3: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `NODE_VERSION` | `20.11.0` |
| `VITE_API_URL` | `https://pokekawaii-backend.onrender.com/api` |

**⚠️ Important:** Replace `pokekawaii-backend.onrender.com` with your actual backend URL from Step A.4

#### Step 4: Configure Redirects/Rewrites

Add a `_redirects` file for SPA routing:

Create `frontend/public/_redirects`:
```
/* /index.html 200
```

Or configure in Render Dashboard:
- Go to **"Redirects/Rewrites"**
- Add rule: `/* → /index.html` (200)

#### Step 5: Deploy Frontend

1. Click **"Create Static Site"**
2. Wait for deployment (2-3 minutes)
3. Access your app at the provided URL

---

## 🔄 Auto-Deploy Setup

Render automatically deploys when you push to GitHub:

1. Go to your service settings
2. Enable **"Auto-Deploy"** (enabled by default)
3. Now every `git push` to `main` branch will trigger deployment

## 📊 Monitoring & Logs

### View Logs

1. Go to your service dashboard
2. Click **"Logs"** tab
3. View real-time logs

### Health Checks

Backend has automatic health check at `/pokemon` endpoint:
- Interval: 30 seconds
- Timeout: 10 seconds
- If fails 3 times, service restarts

### Metrics

Monitor your service:
- CPU usage
- Memory usage
- Bandwidth
- Response time

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain

1. Go to service **"Settings"**
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `pokekawaii.yourdomain.com`
5. Add DNS record (Render provides instructions):
   ```
   Type: CNAME
   Name: pokekawaii
   Value: pokekawaii-frontend.onrender.com
   ```
6. Wait for DNS propagation (5-60 minutes)

### SSL Certificate

Render automatically provisions free SSL certificates via Let's Encrypt.

---

## ⚙️ Environment Variables Reference

### Backend Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.11.0` | Python runtime version |
| `ENVIRONMENT` | `production` | Environment identifier |
| `PORT` | Auto-generated | Port number (Render sets this) |

### Frontend Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `NODE_VERSION` | `20.11.0` | Node.js runtime version |
| `VITE_API_URL` | Backend URL + `/api` | API endpoint for frontend |

---

## 🐛 Troubleshooting

### Issue 1: Backend Deploy Fails

**Symptoms:** Build fails with dependency errors

**Solution:**
```bash
# Check requirements.txt is valid
cat backend/requirements.txt

# Ensure all dependencies have versions
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
python-multipart==0.0.6
```

### Issue 2: Frontend Can't Connect to Backend

**Symptoms:** API calls fail with CORS or network errors

**Solution:**

1. **Check VITE_API_URL:**
   - Go to frontend service → Environment
   - Ensure `VITE_API_URL` = `https://your-backend.onrender.com/api`
   - Click **"Save Changes"** to redeploy

2. **Check CORS in Backend:**
   - Verify `app/main.py` has correct CORS settings:
   ```python
   from fastapi.middleware.cors import CORSMiddleware

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Or specify frontend URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Check Backend Health:**
   - Visit: `https://your-backend.onrender.com/docs`
   - Test: `https://your-backend.onrender.com/pokemon`

### Issue 3: Service Sleeps (Free Plan)

**Symptoms:** First request after inactivity is slow (30s+)

**Cause:** Render free tier spins down after 15 minutes of inactivity

**Solutions:**
- Upgrade to paid plan ($7/month) for always-on
- Accept the cold start delay (typical for free tier)
- Use a cron job to ping your service every 10 minutes (keep-alive)

**Keep-Alive Service (Optional):**
```yaml
# Add to render.yaml
- type: cron
  name: pokekawaii-keepalive
  schedule: "*/10 * * * *"  # Every 10 minutes
  dockerCommand: curl https://pokekawaii-backend.onrender.com/pokemon
```

### Issue 4: Build Timeout

**Symptoms:** Build exceeds time limit

**Solution:**
- Free tier has 15-minute build limit
- Optimize build:
  ```bash
  # Frontend: Use npm ci instead of npm install
  npm ci --only=production && npm run build
  ```

### Issue 5: Static Site 404 on Routes

**Symptoms:** Frontend routes return 404 on refresh

**Solution:**

Create `frontend/public/_redirects`:
```
/*    /index.html   200
```

Or add in Render Dashboard → Redirects/Rewrites.

---

## 📈 Performance Optimization

### 1. Enable Compression

Frontend static assets are automatically compressed by Render's CDN.

### 2. Caching Headers

Add to `frontend/public/_headers`:
```
/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.js
  Cache-Control: public, max-age=31536000, immutable

/*.css
  Cache-Control: public, max-age=31536000, immutable
```

### 3. Select Closest Region

Choose region closest to your users:
- **Singapore**: Asia-Pacific
- **Frankfurt**: Europe
- **Oregon**: US West Coast
- **Ohio**: US East Coast

### 4. Monitor Performance

Use Render's built-in metrics:
- Response time
- Error rate
- Memory usage
- CPU usage

---

## 💰 Pricing

### Free Tier Limits

**Static Sites:**
- ✅ 100 GB bandwidth/month
- ✅ Unlimited sites
- ✅ Auto SSL
- ✅ Global CDN

**Web Services:**
- ✅ 750 hours/month (enough for 1 service always-on)
- ✅ Spins down after 15 min inactivity
- ✅ 512 MB RAM
- ⚠️ Shared CPU

### Paid Plans (Optional)

**Starter ($7/month per service):**
- ✅ Always-on (no spin down)
- ✅ 512 MB RAM
- ✅ Faster cold starts

**Standard ($25/month per service):**
- ✅ 2 GB RAM
- ✅ Dedicated CPU
- ✅ Priority support

---

## 🔐 Security Best Practices

### 1. Environment Variables

- Never commit `.env` files
- Use Render's environment variables UI
- Rotate secrets regularly

### 2. CORS Configuration

Update `backend/app/main.py`:
```python
# Restrict CORS to your frontend domain
allow_origins=[
    "https://pokekawaii-frontend.onrender.com",
    "http://localhost:3000",  # Development
]
```

### 3. Rate Limiting

Consider adding rate limiting to backend:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

## 🔄 CI/CD Workflow

Render auto-deploys on git push:

```
Local Changes → Git Push → GitHub → Render Build → Deploy
```

### Deployment Workflow:

1. Make code changes locally
2. Test locally: `npm run dev` (frontend) + `python run.py` (backend)
3. Commit changes: `git commit -m "Your message"`
4. Push to GitHub: `git push origin main`
5. Render automatically detects push
6. Builds and deploys both services
7. Check deploy logs in Render Dashboard

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Status Page](https://status.render.com/)
- [Render Community Forum](https://community.render.com/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Vite Static Deploy Guide](https://vitejs.dev/guide/static-deploy.html)

---

## 🎉 Quick Checklist

Before deploying, ensure:

- ✅ Code pushed to GitHub (`git push origin main`)
- ✅ `render.yaml` exists in repository root
- ✅ Backend `requirements.txt` has all dependencies
- ✅ Frontend `package.json` has build script
- ✅ API URL environment variable configured
- ✅ CORS enabled in backend
- ✅ SPA redirects configured for frontend

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Render Logs:** Service → Logs tab
2. **Test Locally:** Ensure app works with Docker/npm
3. **Community:** [Render Community Forum](https://community.render.com/)
4. **Support:** Free tier has community support, paid plans have email support

---

**🎮 Enjoy your deployed PokeKawaii game! 🚀**

Your live app: `https://pokekawaii-frontend.onrender.com`
