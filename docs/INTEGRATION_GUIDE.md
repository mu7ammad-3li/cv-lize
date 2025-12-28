# CV Wizard - Frontend-Backend Integration Guide

## Overview

This document provides a comprehensive guide for the CV Wizard full-stack application integration, covering both frontend (React + Vite) and backend (FastAPI) components.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│                    http://localhost:5173                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Frontend (React/Vite)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Components:                                         │   │
│  │  - HomePage                                          │   │
│  │  - FileUpload (drag & drop)                         │   │
│  │  - CVAnalysis                                        │   │
│  │  - ProfessionalResumeDisplay                        │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Client (axios):                                │   │
│  │  - uploadCV()                                        │   │
│  │  - analyzeCV()                                       │   │
│  │  - downloadPDF/DOCX/Markdown()                      │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ REST API (JSON)
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│                  http://localhost:8000                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Routes:                                             │   │
│  │  POST /api/upload                                    │   │
│  │  POST /api/analyze                                   │   │
│  │  GET  /api/download/{id}/{format}                   │   │
│  │  GET  /api/session/{id}                             │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Services:                                           │   │
│  │  - OpenRouter AI (analysis)                         │   │
│  │  - spaCy NLP (parsing)                              │   │
│  │  - PDF/DOCX generators                              │   │
│  │  - ATS validator                                     │   │
│  │  - Keyword analyzer                                  │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   MongoDB Atlas                              │
│                   (Data Persistence)                         │
│  - CV sessions                                               │
│  - Analysis results                                          │
│  - Optimized resumes                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Starting Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or: . venv/bin/activate
python main.py
# Running on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Running on http://localhost:5173
```

**Access the Application:**
- Frontend UI: http://localhost:5173
- Backend API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## Frontend Architecture

### Technology Stack

- **Framework:** React 19.2.3
- **Build Tool:** Vite 7.3.0
- **Language:** TypeScript 5.9.3
- **Styling:** Tailwind CSS 4.1.18
- **UI Components:** Radix UI + Custom Components
- **HTTP Client:** Axios 1.13.2
- **File Upload:** react-dropzone 14.3.8
- **Animations:** Framer Motion 12.23.26
- **Markdown:** react-markdown 10.1.0

### Project Structure

```
frontend/
├── src/
│   ├── main.tsx                 # App entry point
│   ├── App.tsx                  # Main app component
│   ├── components/
│   │   ├── HomePage.tsx         # Landing page
│   │   ├── FileUpload.tsx       # Drag & drop upload
│   │   ├── CVAnalysis.tsx       # Analysis results display
│   │   ├── ProfessionalResumeDisplay.tsx
│   │   ├── StructuredCVDisplay.tsx
│   │   └── ui/                  # Reusable UI components
│   ├── lib/
│   │   ├── api.ts               # API client & types
│   │   ├── utils.ts             # Utility functions
│   │   └── templateDataTransformer.ts
│   └── styles/
├── public/                      # Static assets
├── package.json
├── vite.config.ts
└── tsconfig.json
```

### API Client Configuration

**Environment Variables** (`.env`):
```bash
VITE_API_URL=http://localhost:8000
```

**API Client** (`src/lib/api.ts`):
```typescript
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
```

### Key API Functions

#### 1. Upload CV
```typescript
export async function uploadCV(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<UploadResponse>("/api/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}
```

#### 2. Analyze CV
```typescript
export async function analyzeCV(
  sessionId: string,
  jobDescription: string,
): Promise<AnalyzeResponse> {
  const response = await api.post<AnalyzeResponse>("/api/analyze", {
    session_id: sessionId,
    job_description: jobDescription,
  });

  return response.data;
}
```

#### 3. Download Files
```typescript
export async function downloadPDF(sessionId: string): Promise<Blob> {
  const response = await api.get(`/api/download/${sessionId}/pdf`, {
    responseType: "blob",
  });
  return response.data;
}

export async function downloadDOCX(sessionId: string): Promise<Blob> {
  const response = await api.get(`/api/download/${sessionId}/docx`, {
    responseType: "blob",
  });
  return response.data;
}
```

---

## Backend Architecture

### Technology Stack

- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn (ASGI)
- **Database:** MongoDB Atlas (Motor)
- **AI/NLP:** OpenRouter AI, spaCy
- **Document Processing:** pdfplumber, python-docx, WeasyPrint
- **Security:** SlowAPI, python-magic

### Project Structure

```
backend/
├── main.py                     # FastAPI app entry
├── models/
│   ├── database.py            # MongoDB models
│   └── schemas.py             # Pydantic schemas
├── routes/
│   ├── upload.py              # POST /api/upload
│   ├── analyze.py             # POST /api/analyze
│   └── download.py            # GET /api/download/*
├── services/
│   ├── openrouter_service.py  # AI analysis
│   ├── nlp_processor.py       # spaCy processing
│   ├── pdf_generator.py       # PDF generation
│   ├── docx_generator.py      # DOCX generation
│   ├── ats_validator.py       # ATS validation
│   └── keyword_analyzer.py    # Keyword matching
├── utils/
│   ├── pdf_validator.py       # Security checks
│   └── file_handler.py
└── middleware/
    └── rate_limit.py          # Rate limiting
```

### Environment Configuration

**`.env` file:**
```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
ENVIRONMENT=development

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/cv_wizard

# AI Service
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENROUTER_MODEL=xiaomi/mimo-v2-flash:free

# Security
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
MAX_FILE_SIZE=10485760

# Storage
UPLOAD_DIR=./uploads
QUARANTINE_DIR=./quarantine
```

---

## Data Flow

### 1. CV Upload Flow

```
User selects PDF
    ↓
Frontend: FileUpload component
    ↓
Validate file (size, type)
    ↓
Create FormData
    ↓
POST /api/upload
    ↓
Backend: upload.py
    ↓
Security validation (magic bytes, PDF structure)
    ↓
Extract text (pdfplumber)
    ↓
NLP processing (spaCy)
    ↓
Store in MongoDB
    ↓
Return: { session_id, parsed_data, extracted_text }
    ↓
Frontend: Display success + parsed data
```

### 2. CV Analysis Flow

```
User enters job description
    ↓
Frontend: CVAnalysis component
    ↓
POST /api/analyze
    {
      session_id: "uuid",
      job_description: "text..."
    }
    ↓
Backend: analyze.py
    ↓
Fetch session from MongoDB
    ↓
OpenRouter AI analysis
    ↓
Keyword analysis (compare CV vs JD)
    ↓
ATS validation
    ↓
Generate optimized CV
    ↓
Update session in MongoDB
    ↓
Return: {
      analysis: { score, strengths, weaknesses, ... },
      optimized_cv: { markdown, sections },
      parsed_resume: { personalInfo, experience, ... }
    }
    ↓
Frontend: Display analysis results + optimized CV
```

### 3. Download Flow

```
User clicks "Download PDF/DOCX"
    ↓
Frontend: CVAnalysis component
    ↓
GET /api/download/{session_id}/pdf
    ↓
Backend: download.py
    ↓
Fetch optimized CV from MongoDB
    ↓
Generate PDF/DOCX
    ↓
Return: File blob
    ↓
Frontend: Trigger browser download
```

---

## Type Safety & Contracts

Both frontend and backend share consistent data structures through TypeScript interfaces and Pydantic models.

### Shared Types

**Upload Response:**
```typescript
// Frontend (TypeScript)
interface UploadResponse {
  session_id: string;
  filename: string;
  file_hash: string;
  extracted_text: string;
  parsed_data: ParsedCVData;
}
```

```python
# Backend (Pydantic)
class UploadResponse(BaseModel):
    session_id: str
    filename: str
    file_hash: str
    extracted_text: str
    parsed_data: ParsedCVData
```

**CV Analysis:**
```typescript
// Frontend
interface CVAnalysis {
  score: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  ats_compatibility: number;
  match_percentage: number;
  missing_keywords?: MissingKeyword[];
  keyword_analysis?: KeywordAnalysis[];
  formatting_issues?: ATSFormattingIssue[];
  semantic_similarity_score?: number;
}
```

---

## CORS Configuration

### Backend (FastAPI)

```python
# main.py
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", 
    "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

### Frontend (Vite)

Vite automatically proxies requests when `VITE_API_URL` is set. No additional CORS configuration needed on frontend.

---

## Error Handling

### Frontend Error Handling

```typescript
try {
  const response = await uploadCV(file);
  onUploadSuccess(response);
} catch (err: any) {
  if (err.response?.status === 413) {
    setError("File too large. Maximum size is 10MB.");
  } else if (err.response?.status === 429) {
    setError("Too many requests. Please try again later.");
  } else {
    setError(err.response?.data?.message || "Upload failed. Please try again.");
  }
}
```

### Backend Error Responses

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if DEBUG else "An unexpected error occurred",
        },
    )
```

---

## Rate Limiting

### Backend Configuration

```python
# middleware/rate_limit.py
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# routes/upload.py
@limiter.limit("10/minute")
async def upload_cv(...)

# routes/analyze.py
@limiter.limit("5/minute")
async def analyze_cv(...)
```

### Frontend Handling

```typescript
if (err.response?.status === 429) {
  setError("Too many requests. Please try again in a minute.");
}
```

---

## Testing the Integration

### 1. Health Check

**Frontend:**
```typescript
import { healthCheck } from "@/lib/api";

const status = await healthCheck();
console.log(status); // { status: "healthy", database: "connected" }
```

**Backend:**
```bash
curl http://localhost:8000/health
```

### 2. Upload Test

**Frontend:**
```typescript
const file = new File(["content"], "resume.pdf", { type: "application/pdf" });
const response = await uploadCV(file);
console.log(response.session_id);
```

**Backend:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@resume.pdf"
```

### 3. Full Flow Test

1. Open http://localhost:5173
2. Click "Get Started"
3. Upload a PDF resume
4. Enter a job description
5. Click "Analyze CV"
6. Review analysis results
7. Download optimized resume (PDF/DOCX)

---

## Production Deployment

### Frontend Deployment (Vercel)

```bash
# Build production bundle
npm run build

# Deploy to Vercel
vercel --prod
```

**Environment Variables (Vercel):**
```
VITE_API_URL=https://your-backend-api.com
```

### Backend Deployment (Render/AWS)

```bash
# Update .env for production
DEBUG=False
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Docker:**
```bash
docker build -t cv-wizard-backend .
docker run -p 8000:8000 --env-file .env cv-wizard-backend
```

---

## Monitoring & Debugging

### Frontend Debugging

**Browser Console:**
- Network tab: Check API requests/responses
- React DevTools: Inspect component state
- Console logs: API errors are logged

### Backend Debugging

**Server Logs:**
```bash
# Watch logs in real-time
tail -f backend/logs/app.log
```

**FastAPI Docs:**
- Interactive API testing: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

---

## Common Issues & Solutions

### Issue 1: CORS Errors

**Symptom:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution:**
1. Check `ALLOWED_ORIGINS` in backend `.env`
2. Ensure frontend is using correct API URL
3. Restart both servers after changes

### Issue 2: 404 Not Found

**Symptom:** API endpoints return 404

**Solution:**
1. Verify backend is running on port 8000
2. Check `VITE_API_URL` in frontend `.env`
3. Ensure `/api` prefix is included in routes

### Issue 3: File Upload Fails

**Symptom:** Upload returns 400 Bad Request

**Solution:**
1. Check file size (max 10MB)
2. Verify file type (PDF only)
3. Check backend logs for validation errors

### Issue 4: MongoDB Connection Failed

**Symptom:** "Database: disconnected" in health check

**Solution:**
1. Verify `MONGODB_URI` in backend `.env`
2. Check MongoDB Atlas network access (whitelist IP)
3. Test connection: `python backend/test_mongodb_detailed.py`

---

## Performance Optimization

### Frontend

- **Code Splitting:** Lazy load heavy components
- **Caching:** Cache API responses with React Query
- **Asset Optimization:** Compress images, use CDN
- **Bundle Size:** Tree-shake unused dependencies

### Backend

- **Database Indexing:** Index session_id, created_at
- **Caching:** Cache AI responses for common JDs
- **Connection Pooling:** MongoDB connection pool
- **File Cleanup:** Schedule cleanup of old sessions

---

## Security Checklist

- [x] CORS properly configured
- [x] Rate limiting enabled
- [x] File type validation (magic bytes)
- [x] File size limits enforced
- [x] Input sanitization (Pydantic)
- [x] Environment variables for secrets
- [x] HTTPS in production
- [x] Content Security Policy headers
- [x] Session expiration (24 hours)
- [x] Secure file deletion

---

## Development Workflow

### Making Changes

1. **Update Backend:**
   ```bash
   cd backend
   # Make changes
   # Server auto-reloads with DEBUG=True
   ```

2. **Update Frontend:**
   ```bash
   cd frontend
   # Make changes
   # Vite HMR updates automatically
   ```

3. **Update Types:**
   - Update `backend/models/schemas.py` (Pydantic)
   - Update `frontend/src/lib/api.ts` (TypeScript)
   - Ensure consistency between frontend/backend types

### Git Workflow

```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
# Create PR
```

---

## Resources

- **Backend API Docs:** See `backend/API_DOCUMENTATION.md`
- **Frontend Docs:** http://localhost:5173 (development)
- **Interactive API:** http://localhost:8000/docs
- **GitHub:** https://github.com/yourusername/cv-wizard

---

**Last Updated:** 2025-12-28  
**Version:** 1.0.0
