# 100% Free Deployment Guide for CV-lize 🆓

This guide shows you how to deploy CV-lize completely **FREE** with no credit card required!

## Free Services Stack

- **Frontend**: Vercel (100% Free)
- **Backend**: Render (100% Free tier - no credit card!)
- **Database**: MongoDB Atlas (Free tier)
- **AI**: OpenRouter (Pay-per-use, ~$0.001 per CV analysis)

---

## Prerequisites

1. **GitHub Account** (free)
2. **Vercel Account** (free, no credit card)
3. **Render Account** (free, no credit card)
4. **MongoDB Atlas Account** (free, no credit card)
5. **OpenRouter Account** (pay-per-use, add $5 credit to start)

---

## Step 1: Set Up MongoDB Atlas (Free)

1. **Create MongoDB Atlas account** at https://www.mongodb.com/cloud/atlas

2. **Create a free cluster**:
   - Click "Build a Database"
   - Choose "M0 FREE" tier
   - Select a region close to you
   - Click "Create"

3. **Create a database user**:
   - Go to "Database Access"
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Create username and password (save these!)
   - Give "Read and write to any database" permission

4. **Whitelist all IPs** (for Render to access):
   - Go to "Network Access"
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere"
   - Enter `0.0.0.0/0`
   - Click "Confirm"

5. **Get your connection string**:
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Example: `mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/cvlize?retryWrites=true&w=majority`

---

## Step 2: Get OpenRouter API Key

1. **Create account** at https://openrouter.ai

2. **Add credits**:
   - Go to "Keys & Settings"
   - Add $5 credit (will last for thousands of CV analyses)
   - Cost: ~$0.001 per CV analysis

3. **Create API key**:
   - Click "Create Key"
   - Copy your API key (starts with `sk-or-v1-`)
   - Save it securely!

---

## Step 3: Push Your Code to GitHub

1. **Initialize git** (if not already):
   ```bash
   cd /media/muhammad/Work/Identity/cv-wizzard
   git init
   ```

2. **Create `.gitignore`** (if not exists):
   ```bash
   echo "backend/venv/" >> .gitignore
   echo "backend/.env" >> .gitignore
   echo "backend/__pycache__/" >> .gitignore
   echo "backend/uploads/" >> .gitignore
   echo "backend/quarantine/" >> .gitignore
   echo "backend/*.log" >> .gitignore
   echo "frontend/node_modules/" >> .gitignore
   echo "frontend/.env" >> .gitignore
   echo "frontend/dist/" >> .gitignore
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Initial commit - CV-lize"
   git branch -M main
   ```

4. **Create GitHub repository**:
   - Go to https://github.com/new
   - Name: `cv-lize`
   - Make it public or private
   - Click "Create repository"

5. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/mu7ammad-3li/cv-lize.git
   git push -u origin main
   ```

---

## Step 4: Deploy Backend to Render (Free)

### Option A: Deploy via Dashboard (Easier)

1. **Create Render account** at https://render.com (no credit card needed!)

2. **Create new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your `cv-lize` repository
   - Click "Connect"

3. **Configure the service**:
   - **Name**: `cv-lize-backend`
   - **Region**: Choose closest to you (Oregon recommended)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command**: 
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Select **Free**

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable" and add:
   
   | Key | Value |
   |-----|-------|
   | `MONGODB_URI` | Your MongoDB Atlas connection string |
   | `OPENROUTER_API_KEY` | Your OpenRouter API key |
   | `ALLOWED_ORIGINS` | `*` (we'll update this after deploying frontend) |
   | `ENVIRONMENT` | `production` |
   | `DEBUG` | `False` |
   | `PYTHON_VERSION` | `3.11` |

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for the first deployment
   - Copy your backend URL (e.g., `https://cv-lize-backend.onrender.com`)

### Option B: Deploy via render.yaml (Automatic)

1. **The `render.yaml` file is already created** in your backend directory

2. **Create new Web Service** on Render:
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the `backend/render.yaml` file
   - Add environment variables manually
   - Deploy

---

## Step 5: Deploy Frontend to Vercel (Free)

1. **Create Vercel account** at https://vercel.com (no credit card needed!)

2. **Import your project**:
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Select the `cv-lize` repository

3. **Configure the project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

4. **Add Environment Variable**:
   - Click "Environment Variables"
   - Add variable:
     - **Name**: `VITE_API_URL`
     - **Value**: Your Render backend URL (e.g., `https://cv-lize-backend.onrender.com`)
   - Click "Add"

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Copy your frontend URL (e.g., `https://cv-lize.vercel.app`)

---

## Step 6: Update Backend CORS Settings

1. **Go to Render Dashboard**
2. **Select your backend service**
3. **Go to "Environment"**
4. **Update `ALLOWED_ORIGINS`**:
   - Change from `*` to your Vercel URL
   - Example: `https://cv-lize.vercel.app`
5. **Save changes** (Render will auto-deploy)

---

## Step 7: Test Your Deployment

1. **Visit your frontend URL** (e.g., `https://cv-lize.vercel.app`)

2. **Test the upload**:
   - Try uploading a sample CV
   - Check if AI analysis works
   - Download the optimized PDF

3. **Check backend health**:
   - Visit `https://your-backend.onrender.com/health`
   - Should return: `{"status": "healthy", "database": "connected"}`

---

## Important Notes About Free Tier

### Render Free Tier Limitations

✅ **Included**:
- 750 hours per month (enough for 24/7 uptime)
- Unlimited bandwidth
- Automatic SSL
- Full Python support with system packages

⚠️ **Limitations**:
- **Spins down after 15 minutes of inactivity** (first request after sleep takes ~30 seconds)
- 512 MB RAM
- Shared CPU

💡 **Solution for Sleep Issue**:
- Use a free uptime monitoring service like [UptimeRobot](https://uptimerobot.com) to ping your backend every 5 minutes
- This keeps your backend awake during active hours

### Vercel Free Tier

✅ **Included**:
- 100 GB bandwidth per month
- Unlimited deployments
- Automatic SSL
- Global CDN

No limitations for your frontend!

### MongoDB Atlas Free Tier

✅ **Included**:
- 512 MB storage (enough for thousands of CVs)
- Shared cluster

---

## Optional: Keep Render Backend Awake (Free)

### Using UptimeRobot (Free)

1. **Create account** at https://uptimerobot.com (free)

2. **Add new monitor**:
   - Monitor Type: HTTP(s)
   - Friendly Name: CV-lize Backend
   - URL: `https://your-backend.onrender.com/health`
   - Monitoring Interval: 5 minutes
   - Click "Create Monitor"

This pings your backend every 5 minutes, keeping it awake!

---

## Automatic Deployments

Both Vercel and Render support automatic deployments:

### Every time you push to GitHub:
- Frontend automatically deploys on Vercel
- Backend automatically deploys on Render

No manual deployment needed after initial setup!

---

## Environment Variables Summary

### Backend (Render)
```env
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/cvlize
OPENROUTER_API_KEY=sk-or-v1-xxxxx
ALLOWED_ORIGINS=https://cv-lize.vercel.app
ENVIRONMENT=production
DEBUG=False
PYTHON_VERSION=3.11
```

### Frontend (Vercel)
```env
VITE_API_URL=https://cv-lize-backend.onrender.com
```

---

## Troubleshooting

### Backend takes 30 seconds on first request
- This is normal on Render free tier (cold start)
- Use UptimeRobot to keep it awake

### "CORS error" in browser console
- Update `ALLOWED_ORIGINS` in Render to match your Vercel URL
- Don't include trailing slash

### "Database connection failed"
- Check MongoDB Atlas Network Access allows `0.0.0.0/0`
- Verify `MONGODB_URI` is correct in Render
- Make sure you replaced `<password>` in connection string

### Upload fails
- Check file size is under 5MB
- Verify backend is running at `/health` endpoint

### AI analysis fails
- Verify OpenRouter API key is valid
- Check you have credits in OpenRouter account
- View Render logs for error details

---

## Cost Breakdown

| Service | Cost | Usage Limit |
|---------|------|-------------|
| Vercel (Frontend) | **$0** | 100 GB bandwidth/month |
| Render (Backend) | **$0** | 750 hours/month (24/7) |
| MongoDB Atlas | **$0** | 512 MB storage |
| OpenRouter (AI) | **~$0.001/CV** | Pay-per-use, $5 = ~5000 CVs |
| UptimeRobot (Optional) | **$0** | 50 monitors |

**Total Monthly Cost: $0 (+ OpenRouter usage)**

---

## Monitoring Your Apps

### Vercel
- Dashboard: https://vercel.com/dashboard
- View deployments, analytics, and logs
- Real-time deployment status

### Render
- Dashboard: https://dashboard.render.com
- View logs in real-time
- Monitor resource usage
- See deployment history

### MongoDB Atlas
- Dashboard: https://cloud.mongodb.com
- View database metrics
- Monitor storage usage

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Test all features
4. 🎯 Add custom domain (optional)
5. 🎯 Set up UptimeRobot to keep backend awake
6. 🎯 Share your CV-lize with the world!

---

## Custom Domain (Optional but Free!)

### For Frontend (Vercel)
1. Buy domain from Namecheap/Google Domains (~$10/year)
2. Go to Vercel → Project Settings → Domains
3. Add your domain
4. Update DNS records as shown
5. SSL certificate is automatic!

### For Backend (Render)
1. Go to Render → Service Settings → Custom Domains
2. Add your domain (e.g., `api.cv-lize.com`)
3. Update DNS records
4. Update frontend `VITE_API_URL`

---

## Support

If you run into issues:
1. Check Render logs for backend errors
2. Check browser console for frontend errors
3. Verify all environment variables are set
4. Test backend health endpoint
5. Check MongoDB Atlas network access

---

**Congratulations!** 🎉 You now have a completely free, production-ready CV-lize deployment!

Total cost: **$0/month** (+ minimal OpenRouter usage)
