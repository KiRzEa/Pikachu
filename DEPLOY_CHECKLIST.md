# 🚀 Render Deployment Checklist

## ✅ Pre-Deployment (Completed)

- [x] Code pushed to GitHub
- [x] `render.yaml` blueprint file created
- [x] Frontend updated to use environment variables
- [x] Backend CORS configured for Render
- [x] SPA redirects configured (`_redirects`)
- [x] Build scripts ready

## 📋 Deployment Steps

### Recommended Approach: Blueprint + Manual

**⚠️ Note:** Render Blueprint YAML only supports backend. Frontend must be deployed manually.

#### Part 1: Deploy Backend (Blueprint)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Click **"New +"** → **"Blueprint"**

2. **Connect Repository**
   - Connect GitHub account
   - Select: `KiRzEa/Pikachu`
   - Render detects `render.yaml` automatically

3. **Review Backend Service**
   - ✅ pokekawaii-backend (Python Web Service)
   - Region: Singapore
   - Plan: Free

4. **Click "Apply"**
   - Wait 3-5 minutes for backend deployment
   - Monitor build logs
   - **Copy the backend URL** (e.g., `https://pokekawaii-backend.onrender.com`)

#### Part 2: Deploy Frontend (Manual)

1. **Create Static Site**
   - Click **"New +"** → **"Static Site"**
   - Connect to `KiRzEa/Pikachu` repository

2. **Configure Frontend**
   - **Name**: `pokekawaii-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

3. **Add Environment Variables**
   - Click **"Advanced"** → **"Add Environment Variable"**
   - Add:
     ```
     NODE_VERSION = 20.11.0
     VITE_API_URL = https://pokekawaii-backend.onrender.com/api
     ```
   - ⚠️ **Replace with your actual backend URL from Part 1**

4. **Configure Redirects**
   - The `_redirects` file is already in `frontend/public/`
   - Render will automatically use it for SPA routing

5. **Deploy Frontend**
   - Click **"Create Static Site"**
   - Wait 2-3 minutes
   - Access your app at the provided URL

6. **Access Your App**
   - Frontend: `https://pokekawaii-frontend.onrender.com`
   - Backend: `https://pokekawaii-backend.onrender.com`
   - API Docs: `https://pokekawaii-backend.onrender.com/docs`

### Option 2: Manual Deployment

See detailed instructions in [README_RENDER.md](README_RENDER.md)

## ⚙️ Post-Deployment

- [ ] Test frontend loads correctly
- [ ] Test API endpoints work
- [ ] Test game functionality (create game, make moves)
- [ ] Check CORS is working (no console errors)
- [ ] Verify health checks are passing
- [ ] Set up auto-deploy (should be enabled by default)

## 🔧 Important URLs to Update

After deploying, update these in your Render Dashboard:

### Backend Service
- **Name**: `pokekawaii-backend`
- **Environment Variables**:
  - `PYTHON_VERSION`: `3.11.0`
  - `ENVIRONMENT`: `production`

### Frontend Service
- **Name**: `pokekawaii-frontend`
- **Environment Variables**:
  - `NODE_VERSION`: `20.11.0`
  - `VITE_API_URL`: `https://pokekawaii-backend.onrender.com/api` ⚠️ Update this!

### Backend CORS (backend/app/main.py)
- Update line 23: Replace `pokekawaii-frontend` with your actual frontend URL
- Or use `"*"` for development (less secure)

## 🐛 Quick Troubleshooting

**Frontend can't connect to backend?**
- Check `VITE_API_URL` in frontend environment variables
- Ensure it ends with `/api`
- Verify CORS allows your frontend domain

**Service won't start?**
- Check build logs in Render Dashboard
- Verify all dependencies in requirements.txt/package.json
- Ensure Python/Node versions match

**404 on routes?**
- Verify `_redirects` file exists in `frontend/public/`
- Check it's included in build output

**First load is slow?**
- Normal for free tier (cold start ~30s)
- Service spins down after 15 min inactivity
- Upgrade to paid tier for always-on

## 📊 Expected Build Times

- **Backend**: 2-4 minutes
- **Frontend**: 1-3 minutes
- **First Deploy**: 5-10 minutes total

## 💡 Tips

- Free tier has 750 hours/month (enough for 1 always-on service)
- Static sites have unlimited bandwidth on free tier
- Auto-deploy works on every `git push` to main branch
- Check logs if deployment fails

## 🎉 Success Indicators

You're successfully deployed when:
- ✅ Both services show "Live" status in Render Dashboard
- ✅ Frontend URL loads the game
- ✅ API docs accessible at `/docs`
- ✅ You can create and play a game
- ✅ No CORS errors in browser console

---

**Need help?** Check [README_RENDER.md](README_RENDER.md) for detailed troubleshooting.
