# CV-lize Deployment Guide

This guide covers deploying CV-lize to Vercel (frontend) and Vercel/Railway/Render (backend).

## Architecture

CV-lize is a full-stack application with:
- **Frontend**: React + Vite + TypeScript
- **Backend**: FastAPI + Python

Both need to be deployed separately.

---

## Option 1: Deploy Frontend to Vercel + Backend to Vercel (Recommended for Quick Start)

### Step 1: Deploy Backend to Vercel

1. **Create a Vercel account** at https://vercel.com

2. **Install Vercel CLI** (optional, but recommended):
   ```bash
   npm install -g vercel
   ```

3. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

4. **Deploy using Vercel CLI**:
   ```bash
   vercel
   ```
   
   Or deploy via Vercel Dashboard:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Set **Root Directory** to `backend`
   - Add environment variables (see below)
   - Deploy

5. **Add Environment Variables** in Vercel Dashboard:
   ```
   MONGODB_URI=your_mongodb_connection_string
   OPENROUTER_API_KEY=your_openrouter_api_key
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ENVIRONMENT=production
   DEBUG=False
   ```

6. **Copy your backend URL** (e.g., `https://cv-lize-backend.vercel.app`)

### Step 2: Deploy Frontend to Vercel

1. **Navigate to frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Create/Update `.env.production`**:
   ```bash
   VITE_API_URL=https://your-backend-url.vercel.app
   ```

3. **Deploy using Vercel CLI**:
   ```bash
   vercel
   ```
   
   Or deploy via Vercel Dashboard:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Set **Root Directory** to `frontend`
   - Add environment variable:
     ```
     VITE_API_URL=https://your-backend-url.vercel.app
     ```
   - Deploy

4. **Update Backend CORS Settings**:
   - Go to your backend Vercel project
   - Update `ALLOWED_ORIGINS` environment variable with your frontend URL
   - Redeploy backend

---

## Option 2: Frontend on Vercel + Backend on Railway (Better for Production)

Railway is better suited for Python backends with background processes and file uploads.

### Step 1: Deploy Backend to Railway

1. **Create a Railway account** at https://railway.app

2. **Create a new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - Set **Root Directory** to `backend`

3. **Add Environment Variables**:
   ```
   MONGODB_URI=your_mongodb_connection_string
   OPENROUTER_API_KEY=your_openrouter_api_key
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ENVIRONMENT=production
   DEBUG=False
   PORT=8000
   HOST=0.0.0.0
   ```

4. **Configure Build Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Deploy** and copy your Railway URL

### Step 2: Deploy Frontend to Vercel

Follow the same steps as Option 1, but use your Railway backend URL in `VITE_API_URL`.

---

## Option 3: Frontend on Vercel + Backend on Render

Render offers a generous free tier and is great for Python applications.

### Step 1: Deploy Backend to Render

1. **Create a Render account** at https://render.com

2. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Set **Root Directory** to `backend`

3. **Configure the service**:
   - **Name**: cv-lize-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**:
   ```
   MONGODB_URI=your_mongodb_connection_string
   OPENROUTER_API_KEY=your_openrouter_api_key
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ENVIRONMENT=production
   DEBUG=False
   PYTHON_VERSION=3.11
   ```

5. **Deploy** and copy your Render URL

### Step 2: Deploy Frontend to Vercel

Follow the same steps as Option 1, but use your Render backend URL in `VITE_API_URL`.

---

## GitHub Deployment (Automatic)

For automatic deployments on every push:

### Frontend (Vercel)

1. **Connect GitHub to Vercel**:
   - Go to https://vercel.com/new
   - Import your repository
   - Set Root Directory to `frontend`
   - Add environment variables
   - Enable automatic deployments

2. **Configure Build Settings** (usually auto-detected):
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

### Backend (Railway/Render)

Both Railway and Render support automatic deployments from GitHub:
- Connect your repository
- Set the root directory to `backend`
- Configure environment variables
- Enable automatic deployments on push

---

## Environment Variables Reference

### Backend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `MONGODB_URI` | MongoDB connection string | Yes | `mongodb+srv://user:pass@cluster.mongodb.net/cvwizard` |
| `OPENROUTER_API_KEY` | OpenRouter API key for AI | Yes | `sk-or-v1-xxxxx` |
| `ALLOWED_ORIGINS` | Frontend URL for CORS | Yes | `https://cv-lize.vercel.app` |
| `ENVIRONMENT` | Environment name | No | `production` |
| `DEBUG` | Debug mode | No | `False` |
| `PORT` | Server port | No | `8000` |
| `HOST` | Server host | No | `0.0.0.0` |

### Frontend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API URL | Yes | `https://cv-lize-backend.vercel.app` |

---

## Post-Deployment Checklist

- [ ] Backend is accessible at `/health` endpoint
- [ ] Frontend can connect to backend API
- [ ] CORS is properly configured
- [ ] Environment variables are set correctly
- [ ] MongoDB connection is working
- [ ] File uploads are working
- [ ] AI analysis is working (OpenRouter API key is valid)
- [ ] PDF generation is working
- [ ] Rate limiting is active

---

## Troubleshooting

### Frontend can't connect to backend
- Check `VITE_API_URL` in frontend environment variables
- Verify backend `ALLOWED_ORIGINS` includes frontend URL
- Check browser console for CORS errors

### Backend deployment fails on Vercel
- Vercel has limitations with serverless Python (file uploads, long-running processes)
- Consider using Railway or Render for the backend instead

### File uploads not working
- Vercel serverless functions have a 4.5 MB body size limit
- Use Railway or Render for handling file uploads

### PDF generation fails
- Some platforms don't support WeasyPrint due to system dependencies
- Consider using a Docker-based deployment or a platform that supports system packages

### MongoDB connection fails
- Verify `MONGODB_URI` is correct
- Check if your IP is whitelisted in MongoDB Atlas (use 0.0.0.0/0 for all IPs)
- Ensure database user has proper permissions

---

## Custom Domain (Optional)

### Vercel
1. Go to your project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### Railway/Render
1. Go to your service settings
2. Navigate to "Custom Domains"
3. Add your domain and update DNS records

---

## Monitoring and Logs

### Vercel
- View logs in the Vercel Dashboard under "Deployments"
- Click on any deployment to see build and runtime logs

### Railway
- View logs in real-time from the Railway dashboard
- Access metrics and resource usage

### Render
- View logs from the "Logs" tab in your service
- Monitor resource usage and deployment status

---

## Cost Considerations

### Free Tier Limits

**Vercel (Frontend)**:
- 100GB bandwidth per month
- Unlimited deployments
- Unlimited websites

**Vercel (Backend - Serverless)**:
- 100GB bandwidth per month
- 100 GB-hours compute time
- ⚠️ Limited for file uploads and long-running processes

**Railway**:
- $5 free credit per month
- ~500 hours of free compute
- Pay-as-you-go after free tier

**Render**:
- Free tier with 750 hours per month
- Sleeps after 15 minutes of inactivity
- Generous for hobby projects

---

## Recommended Setup

For **Development/Hobby Projects**:
- Frontend: Vercel
- Backend: Render (free tier)
- Database: MongoDB Atlas (free tier)

For **Production**:
- Frontend: Vercel
- Backend: Railway or Render (paid)
- Database: MongoDB Atlas (paid tier with backups)
- CDN: Cloudflare (optional, free)

---

## Next Steps

1. Set up MongoDB Atlas database
2. Get OpenRouter API key from https://openrouter.ai
3. Deploy backend first
4. Deploy frontend with backend URL
5. Test all functionality
6. Set up custom domain (optional)
7. Enable monitoring and analytics

Happy deploying! 🚀
