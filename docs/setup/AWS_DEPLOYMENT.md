# AWS Free Tier Deployment Guide for CV-lize 🚀

Deploy CV-lize completely **FREE** using AWS Free Tier services!

## AWS Free Tier Services We'll Use

| Service | Free Tier | What We Use It For |
|---------|-----------|-------------------|
| **EC2 (t2.micro)** | 750 hours/month (1 year) | Backend hosting |
| **S3** | 5 GB storage | Static frontend hosting |
| **CloudFront** | 50 GB data transfer | CDN for frontend |
| **Elastic IP** | 1 free (when attached) | Static IP for backend |
| **Route 53** | $0.50/month per hosted zone | DNS (optional) |

**Total Monthly Cost**: **$0** for first 12 months (within free tier limits)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Users                          │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│         CloudFront (CDN - Free)                 │
│         Caches and serves frontend              │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│         S3 Bucket (Frontend - Free)             │
│         React + Vite static files               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│         EC2 t2.micro (Backend - Free)           │
│         FastAPI + Docker                        │
│         + Elastic IP (Free)                     │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│         MongoDB Atlas (Free Tier)               │
│         Database (outside AWS)                  │
└─────────────────────────────────────────────────┘
```

---

## Prerequisites

1. **AWS Account** (Free tier eligible)
2. **MongoDB Atlas Account** (Free tier)
3. **OpenRouter API Key** ($5 credit)
4. **Domain Name** (Optional - ~$10/year)
5. **Basic Linux knowledge**

---

## Part 1: Set Up MongoDB Atlas

Follow the same steps from `FREE_DEPLOYMENT.md`:

1. Create MongoDB Atlas free cluster
2. Create database user
3. Whitelist all IPs (0.0.0.0/0)
4. Get connection string

---

## Part 2: Deploy Backend to EC2 (Free Tier)

### Step 1: Launch EC2 Instance

1. **Sign in to AWS Console** → Go to EC2 Dashboard

2. **Launch Instance**:
   - Click "Launch Instance"
   - **Name**: `cv-lize-backend`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: `t2.micro` (Free tier eligible - 1GB RAM, 1 vCPU)
   - **Key pair**: Create new key pair
     - Name: `cv-lize-key`
     - Type: RSA
     - Format: .pem
     - Download and save the key file

3. **Network Settings**:
   - Click "Edit"
   - **Auto-assign public IP**: Enable
   - **Firewall (Security Group)**:
     - Create security group: `cv-lize-backend-sg`
     - Add rules:
       - SSH (22) - Your IP only (for security)
       - HTTP (80) - Anywhere (0.0.0.0/0)
       - HTTPS (443) - Anywhere (0.0.0.0/0)
       - Custom TCP (8000) - Anywhere (0.0.0.0/0)

4. **Storage**:
   - Keep default: 8 GB gp2 (Free tier: 30 GB)
   - Can increase to 30 GB for free

5. **Launch Instance** and wait for it to start

### Step 2: Allocate Elastic IP (Optional but Recommended)

1. Go to **EC2 → Elastic IPs**
2. Click "Allocate Elastic IP address"
3. Click "Allocate"
4. Select the new Elastic IP → Actions → **Associate Elastic IP address**
5. Select your `cv-lize-backend` instance
6. Click "Associate"

**Note**: Elastic IP is free when attached to a running instance!

### Step 3: Connect to Your EC2 Instance

1. **Get the public IP** from EC2 Dashboard

2. **Set key permissions** (on your local machine):
   ```bash
   chmod 400 cv-lize-key.pem
   ```

3. **Connect via SSH**:
   ```bash
   ssh -i cv-lize-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
   ```

### Step 4: Install Docker on EC2

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Exit and reconnect to apply group changes
exit
```

Reconnect via SSH again:
```bash
ssh -i cv-lize-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 5: Install Docker Compose

```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 6: Clone Your Repository

```bash
# Install git
sudo apt install git -y

# Clone your repository
git clone https://github.com/mu7ammad-3li/cv-lize.git
cd cv-lize/backend
```

### Step 7: Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add your environment variables:
```env
MONGODB_URI=your_mongodb_atlas_connection_string
OPENROUTER_API_KEY=your_openrouter_api_key
ALLOWED_ORIGINS=*
ENVIRONMENT=production
DEBUG=False
PORT=8000
HOST=0.0.0.0
```

Save: `Ctrl + O`, `Enter`, `Ctrl + X`

### Step 8: Build and Run with Docker

```bash
# Build and start the container
docker-compose up -d --build

# Check if it's running
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 9: Test Backend

```bash
# Test locally on EC2
curl http://localhost:8000/health

# Test from your computer
curl http://YOUR_EC2_PUBLIC_IP:8000/health
```

You should see: `{"status": "healthy", "database": "connected"}`

### Step 10: Set Up Auto-Restart (Optional)

```bash
# Edit docker-compose.yml to ensure auto-restart
# (Already configured with: restart: unless-stopped)

# Enable Docker to start on boot
sudo systemctl enable docker
```

---

## Part 3: Deploy Frontend to S3 + CloudFront

### Step 1: Build Frontend Locally

On your local machine:

```bash
cd /media/muhammad/Work/Identity/cv-wizzard/frontend

# Create production environment file
echo "VITE_API_URL=http://YOUR_EC2_PUBLIC_IP:8000" > .env.production

# Build for production
npm run build
```

### Step 2: Create S3 Bucket

1. **Go to S3 Console** → Click "Create bucket"

2. **Configure bucket**:
   - **Bucket name**: `cv-lize-frontend` (must be globally unique)
   - **Region**: Choose closest to your users
   - **Block Public Access**: Uncheck "Block all public access"
   - **Acknowledge**: Check the warning box
   - Click "Create bucket"

3. **Upload build files**:
   - Click on your bucket
   - Click "Upload"
   - Drag and drop all files from `frontend/dist/` folder
   - Click "Upload"

4. **Enable Static Website Hosting**:
   - Go to bucket → "Properties" tab
   - Scroll to "Static website hosting"
   - Click "Edit"
   - Enable it
   - **Index document**: `index.html`
   - **Error document**: `index.html` (for SPA routing)
   - Save changes
   - Copy the **Bucket website endpoint** URL

5. **Set Bucket Policy** (make files public):
   - Go to "Permissions" tab
   - Scroll to "Bucket policy"
   - Click "Edit"
   - Paste this policy (replace `YOUR-BUCKET-NAME`):

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
       }
     ]
   }
   ```
   - Save changes

### Step 3: Set Up CloudFront CDN (Optional but Recommended)

1. **Go to CloudFront Console** → Click "Create Distribution"

2. **Configure Distribution**:
   - **Origin Domain**: Select your S3 bucket website endpoint
     - Use the website endpoint, not the bucket name
     - Example: `cv-lize-frontend.s3-website-us-east-1.amazonaws.com`
   - **Viewer Protocol Policy**: Redirect HTTP to HTTPS
   - **Allowed HTTP Methods**: GET, HEAD, OPTIONS
   - **Cache Policy**: CachingOptimized
   - **Default Root Object**: `index.html`

3. **Error Pages** (for SPA routing):
   - After creating distribution, go to "Error Pages" tab
   - Create custom error response:
     - **HTTP Error Code**: 403
     - **Customize Error Response**: Yes
     - **Response Page Path**: `/index.html`
     - **HTTP Response Code**: 200
   - Create another:
     - **HTTP Error Code**: 404
     - **Response Page Path**: `/index.html`
     - **HTTP Response Code**: 200

4. **Create Distribution** and wait (5-10 minutes)

5. **Copy CloudFront URL** (e.g., `d111111abcdef8.cloudfront.net`)

### Step 4: Update Backend CORS

```bash
# SSH back to EC2
ssh -i cv-lize-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

cd cv-lize/backend

# Edit .env
nano .env
```

Update `ALLOWED_ORIGINS`:
```env
ALLOWED_ORIGINS=https://YOUR-CLOUDFRONT-DOMAIN.cloudfront.net
```

Save and restart:
```bash
docker-compose restart
```

---

## Part 4: Use NGINX Reverse Proxy (Recommended)

To serve backend on port 80/443 instead of 8000:

### Step 1: Install NGINX

```bash
sudo apt install nginx -y
```

### Step 2: Configure NGINX

```bash
sudo nano /etc/nginx/sites-available/cv-lize-backend
```

Paste this configuration:
```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Save and enable:
```bash
sudo ln -s /etc/nginx/sites-available/cv-lize-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Update `.env`:
```bash
nano .env
```

Change ALLOWED_ORIGINS to use http:
```env
ALLOWED_ORIGINS=https://YOUR-CLOUDFRONT-DOMAIN.cloudfront.net,http://YOUR_EC2_PUBLIC_IP
```

Restart backend:
```bash
docker-compose restart
```

---

## Part 5: Add SSL Certificate (Free with Let's Encrypt)

### Step 1: Get a Domain (Optional)

- Buy a domain from Route 53, Namecheap, or Google Domains
- Point it to your EC2 Elastic IP

### Step 2: Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Step 3: Get SSL Certificate

```bash
sudo certbot --nginx -d api.yourdomain.com
```

Follow the prompts. Certbot will automatically configure NGINX for HTTPS.

### Step 4: Auto-Renewal

```bash
sudo systemctl status certbot.timer
```

Certbot automatically renews certificates!

---

## Automated Deployment Script

Create this script on EC2 for easy updates:

```bash
nano ~/update-backend.sh
```

Paste:
```bash
#!/bin/bash
cd ~/cv-lize/backend
git pull
docker-compose down
docker-compose up -d --build
docker-compose logs -f
```

Make executable:
```bash
chmod +x ~/update-backend.sh
```

Use it to update:
```bash
~/update-backend.sh
```

---

## Monitoring and Maintenance

### View Logs

```bash
cd ~/cv-lize/backend
docker-compose logs -f
```

### Check Resource Usage

```bash
# CPU and Memory
htop

# Disk usage
df -h

# Docker stats
docker stats
```

### Backup Strategy

1. **MongoDB**: Atlas handles backups automatically
2. **Uploaded files**: Sync to S3 periodically
   ```bash
   aws s3 sync ~/cv-lize/backend/uploads s3://cv-lize-uploads-backup/
   ```

---

## AWS Free Tier Limits to Watch

| Service | Free Tier | What Happens After |
|---------|-----------|-------------------|
| EC2 t2.micro | 750 hrs/month (12 months) | Charged per hour (~$8/month) |
| S3 Storage | 5 GB | $0.023/GB/month |
| S3 Requests | 20K GET, 2K PUT | $0.0004 per 1K requests |
| CloudFront | 50 GB data transfer | $0.085/GB |
| Elastic IP | Free when attached | $0.005/hour if not attached |

**Tip**: Set up AWS Budget alerts to monitor usage!

---

## Cost Optimization Tips

1. **Stop EC2 when not in use** (dev/staging environments)
2. **Use CloudFront** to reduce S3 data transfer costs
3. **Enable S3 lifecycle policies** to delete old uploads
4. **Monitor with CloudWatch** (free tier: 10 custom metrics)
5. **Set up billing alerts** at $1, $5, $10

---

## Security Best Practices

1. **Use Security Groups properly**:
   - Only allow SSH from your IP
   - Use HTTPS in production

2. **Update System Regularly**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Use Environment Variables**:
   - Never commit .env files
   - Use AWS Secrets Manager for sensitive data

4. **Enable AWS CloudTrail** (free tier):
   - Monitor API calls and user activity

5. **Regular Backups**:
   - Set up automated backups for uploads
   - MongoDB Atlas handles database backups

---

## Troubleshooting

### EC2 Instance Won't Start
- Check if you've exceeded free tier hours (750/month)
- Verify instance type is t2.micro

### Can't Connect via SSH
- Check Security Group allows SSH from your IP
- Verify key file permissions: `chmod 400 cv-lize-key.pem`

### Docker Container Crashes
```bash
# Check logs
docker-compose logs

# Check memory
free -h

# t2.micro has 1GB RAM - may need to optimize
```

### Frontend Shows CORS Error
- Update backend ALLOWED_ORIGINS
- Check CloudFront URL is correct in frontend build

### S3 Files Not Accessible
- Check bucket policy allows public read
- Verify files were uploaded correctly

---

## Alternative: AWS Amplify (Even Easier!)

AWS Amplify can host your frontend for free:

1. **Go to Amplify Console**
2. **Connect GitHub repository**
3. **Select frontend branch**
4. **Add environment variable**: `VITE_API_URL=http://YOUR_EC2_IP`
5. **Deploy**

Free tier: 1000 build minutes/month, 15 GB storage

---

## Cost Comparison After Free Tier (12 months)

| Component | Monthly Cost |
|-----------|-------------|
| EC2 t2.micro (750 hrs) | ~$8.50 |
| S3 Storage (5 GB) | ~$0.12 |
| CloudFront (50 GB) | ~$4.25 |
| Elastic IP | $0 (attached) |
| **Total** | **~$13/month** |

Still cheaper than most hosting providers!

---

## Scaling Beyond Free Tier

When you outgrow free tier:
1. **Upgrade to t3.small** for more RAM (~$15/month)
2. **Use Application Load Balancer** for high availability
3. **Add Auto Scaling Group** for traffic spikes
4. **Move to ECS/Fargate** for container orchestration
5. **Use RDS** instead of MongoDB Atlas

---

## Summary

✅ **Free for 12 months** (within AWS free tier limits)
✅ **Full control** over infrastructure
✅ **Scalable** when needed
✅ **Professional setup** with NGINX, SSL, Docker
✅ **Auto-deployment** via git pull

**Next Steps**:
1. Launch EC2 instance
2. Install Docker and deploy backend
3. Create S3 bucket and upload frontend
4. Set up CloudFront CDN
5. Configure NGINX and SSL
6. Monitor usage to stay within free tier!

Happy deploying on AWS! 🚀☁️
