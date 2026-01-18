# 🔄 Frontend Redeploy Instructions

## Issue: 404 Error on Assets

If you're seeing 404 errors for JavaScript/CSS files like:
```
GET /assets/index-BvKsaynw.js → 404 Not Found
```

## ✅ Solution Applied

Updated `vite.config.js` with proper build configuration:
- Set `base: '/'` for correct asset paths
- Configured build output directories
- Added manifest generation
- Fixed rollup output options

## 🚀 Redeploy Frontend

### Option 1: Automatic (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Select your frontend service** (e.g., `pikachu-fe`)
3. **Wait for auto-deploy** (Render detects the git push)
4. Monitor the "Events" tab for deployment progress

### Option 2: Manual Deploy

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Select your frontend service** (e.g., `pikachu-fe`)
3. Click **"Manual Deploy"** dropdown
4. Select **"Clear build cache & deploy"**
5. Wait 2-3 minutes for rebuild

## 📋 Verify Fix

After deployment completes:

1. **Clear browser cache** (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
2. **Visit your frontend URL**: `https://pikachu-fe.onrender.com`
3. **Open DevTools Console** (F12) → Check for errors
4. **Test the game**:
   - Click "New Game"
   - Try making moves
   - Check if API calls work

## 🔍 Expected Results

✅ No 404 errors in Network tab
✅ JavaScript files load successfully
✅ Game UI appears correctly
✅ API calls to backend work

## 🐛 If Still Getting 404s

1. **Check build output**:
   - Go to Render Dashboard → Service → "Logs" tab
   - Look for build completion: `✓ built in XXXms`
   - Verify files are in `dist/` directory

2. **Verify publish directory**:
   - Service Settings → Build & Deploy
   - Publish Directory should be: `dist`
   - Root Directory should be: `frontend`

3. **Check environment variables**:
   - Ensure `VITE_API_URL` is set correctly
   - Should be: `https://your-backend.onrender.com/api`

4. **Test build locally**:
   ```bash
   cd frontend
   npm run build
   ls -la dist/
   ls -la dist/assets/
   ```

## 📊 Build Output Should Look Like

```
frontend/dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── [other assets]
└── _redirects
```

## 🆘 Common Issues

### Issue: Assets still 404
**Solution**: Clear build cache and redeploy

### Issue: Blank page
**Solution**: Check browser console for errors, verify VITE_API_URL

### Issue: CORS errors
**Solution**: Verify backend CORS allows your frontend domain

---

**Last Updated**: After vite.config.js fix
