# CV Wizard - Setup Guide

## Quick Start (Backend)

### 1. Prerequisites

- Python 3.11+
- MongoDB Atlas account (free M0 tier)
- Google Gemini API key (free tier)

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_md
```

### 3. Environment Configuration

Create `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# MongoDB Atlas Connection
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cv-wizard?retryWrites=true&w=majority

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings
ENVIRONMENT=development
DEBUG=True
PORT=8000
HOST=0.0.0.0

# File Upload Settings
MAX_FILE_SIZE=5242880  # 5MB
UPLOAD_DIR=./uploads
QUARANTINE_DIR=./quarantine

# Security
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_WINDOW=900

# Session Settings
SESSION_TTL_HOURS=24
```

### 4. Get MongoDB Atlas URI

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free M0 cluster
3. Create database user
4. Whitelist your IP (or 0.0.0.0/0 for development)
5. Get connection string from "Connect" → "Connect your application"
6. Replace `<password>` and `<username>` in the URI

### 5. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy and paste into `.env`

### 6. Run the Backend

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate

# Run with uvicorn
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## Testing the API

### 1. Upload a CV

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@/path/to/your/resume.pdf"
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "resume.pdf",
  "file_hash": "a1b2c3...",
  "extracted_text": "...",
  "parsed_data": {
    "skills": ["Python", "FastAPI"],
    "experience": [],
    "education": [],
    "contact": {...}
  }
}
```

### 2. Analyze CV

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "job_description": "We are looking for a Python developer with FastAPI experience..."
  }'
```

### 3. Download Optimized CV

```bash
# Download as Markdown
curl "http://localhost:8000/api/download/{session_id}/markdown" \
  -o optimized_resume.md

# Download as PDF (TODO)
curl "http://localhost:8000/api/download/{session_id}/pdf" \
  -o optimized_resume.pdf
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### spaCy Model Not Found

```bash
python -m spacy download en_core_web_md
```

If you have limited bandwidth, use the smaller model:
```bash
python -m spacy download en_core_web_sm
```

### MongoDB Connection Error

- Check if your IP is whitelisted in MongoDB Atlas
- Verify the connection string format
- Ensure database user has correct permissions

### Gemini API Rate Limit

Free tier limits:
- 5 requests per minute
- ~20-25 requests per day

The API implements caching to reduce redundant calls.

### Import Errors

Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Next Steps

1. ✅ Backend API is running
2. 🔄 Create frontend React application
3. 🔄 Implement PDF generation
4. 🔄 Add Docker configuration
5. 🔄 Deploy to AWS EC2

## Development Tips

### Auto-reload on Changes

```bash
uvicorn main:app --reload
```

### View Logs

Logs are printed to console. For production, configure proper logging.

### Database Management

View your data in MongoDB Atlas:
1. Go to your cluster
2. Click "Browse Collections"
3. Navigate to `cv_wizard` database → `cv_sessions` collection

### Security Testing

Test PDF security validation with a malicious pattern:
```bash
# This will be rejected
echo "%PDF-1.4\n/JavaScript (alert(1))" > test.pdf
curl -X POST "http://localhost:8000/api/upload" -F "file=@test.pdf"
```

## Production Deployment

See `DEPLOYMENT.md` (to be created) for AWS EC2 deployment instructions.

## Support

For issues or questions:
- Check API documentation at `/docs`
- Review logs in console
- Check MongoDB Atlas dashboard
- Verify environment variables in `.env`
