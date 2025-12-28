# CV Wizard Backend API Documentation

## Overview

The CV Wizard Backend is a FastAPI-based REST API that provides AI-powered CV optimization and ATS (Applicant Tracking System) compatibility analysis. It uses OpenRouter AI for intelligent analysis, spaCy for NLP processing, and MongoDB for data persistence.

**Base URL:** `http://localhost:8000` (development)  
**API Version:** 1.0.0  
**Interactive Docs:** `http://localhost:8000/docs`

## Table of Contents

- [Architecture](#architecture)
- [Setup & Configuration](#setup--configuration)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Security Features](#security-features)
- [Testing](#testing)

---

## Architecture

### Technology Stack

- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn (ASGI)
- **Database:** MongoDB Atlas (Motor async driver)
- **AI/NLP:**
  - OpenRouter AI (via OpenAI SDK)
  - spaCy (en_core_web_md)
- **Document Processing:**
  - PDF: pdfplumber, PyPDF2
  - PDF Generation: WeasyPrint
  - DOCX Generation: python-docx
- **Security:** SlowAPI (rate limiting), python-magic (file validation)

### Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── models/
│   ├── database.py        # MongoDB connection & models
│   └── schemas.py         # Pydantic schemas
├── routes/
│   ├── upload.py          # File upload endpoint
│   ├── analyze.py         # CV analysis endpoint
│   └── download.py        # Download endpoints (PDF, DOCX, Markdown)
├── services/
│   ├── openrouter_service.py  # AI analysis service
│   ├── nlp_processor.py       # spaCy NLP processing
│   ├── pdf_generator.py       # PDF generation
│   ├── docx_generator.py      # DOCX generation (ATS-optimized)
│   ├── markdown_parser.py     # Markdown parsing
│   ├── ats_validator.py       # ATS compliance validation
│   └── keyword_analyzer.py    # Keyword analysis & matching
├── utils/
│   ├── pdf_validator.py   # PDF security validation
│   └── file_handler.py    # File handling utilities
└── middleware/
    └── rate_limit.py      # Rate limiting configuration
```

---

## Setup & Configuration

### Prerequisites

- Python 3.12+
- MongoDB Atlas account
- OpenRouter API key

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
ENVIRONMENT=development

# Database
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cv_wizard

# AI Service
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENROUTER_MODEL=xiaomi/mimo-v2-flash:free  # or nvidia/llama-3.1-nemotron-70b-instruct

# Security
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
MAX_FILE_SIZE=10485760  # 10MB in bytes

# File Storage
UPLOAD_DIR=./uploads
QUARANTINE_DIR=./quarantine
```

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_md

# Run setup test
python test_setup.py
```

### Starting the Server

```bash
# Development (with auto-reload)
python main.py

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## API Endpoints

### 1. Health Check

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "message": "CV Wizard API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "endpoints": {
    "upload": "POST /api/upload",
    "analyze": "POST /api/analyze",
    "download_markdown": "GET /api/download/{session_id}/markdown",
    "download_pdf": "GET /api/download/{session_id}/pdf",
    "get_session": "GET /api/session/{session_id}"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### 2. Upload CV

#### `POST /api/upload`
Upload a CV file (PDF) for processing.

**Headers:**
```
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: PDF file (max 10MB)

**Rate Limit:** 10 requests per minute

**Response:** `200 OK`
```json
{
  "session_id": "9b229850-d7ee-4588-8d2d-f8f72a745d87",
  "filename": "resume.pdf",
  "file_hash": "232ac6b7eb8ac9f4e7087a40cb214779...",
  "extracted_text": "JOHN DOE\nSoftware Engineer...",
  "parsed_data": {
    "skills": ["Python", "JavaScript", "AWS"],
    "experience": [
      {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "duration": "2020-2023",
        "description": "Developed web applications...",
        "start_date": "2020-01-01",
        "end_date": "2023-12-31"
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Computer Science",
        "institution": "University",
        "year": "2020",
        "gpa": "3.8",
        "honors": "Magna Cum Laude"
      }
    ],
    "contact": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "linkedin": "linkedin.com/in/johndoe",
      "location": "San Francisco, CA"
    }
  }
}
```

**Errors:**
- `400`: Invalid file type or corrupted PDF
- `413`: File too large
- `429`: Rate limit exceeded

**Example:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@resume.pdf"
```

---

### 3. Analyze CV

#### `POST /api/analyze`
Analyze CV against a job description using AI.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "session_id": "9b229850-d7ee-4588-8d2d-f8f72a745d87",
  "job_description": "We are looking for a Full Stack Developer with experience in React, Node.js, and AWS..."
}
```

**Rate Limit:** 5 requests per minute

**Response:** `200 OK`
```json
{
  "analysis": {
    "score": 88,
    "strengths": [
      "Strong technical background in React and Node.js",
      "Clear demonstration of impact with quantifiable metrics",
      "Well-organized structure"
    ],
    "weaknesses": [
      "Missing specific AWS certifications",
      "Could emphasize leadership experience more"
    ],
    "suggestions": [
      "Add AWS certifications if available",
      "Include more quantifiable metrics",
      "Highlight team collaboration experiences"
    ],
    "ats_compatibility": 95,
    "match_percentage": 92,
    "missing_keywords": [
      {
        "keyword": "Kubernetes",
        "category": "infrastructure",
        "importance": "high",
        "suggestion": "Add Kubernetes experience if available"
      }
    ],
    "keyword_analysis": [
      {
        "keyword": "React",
        "frequency": 8,
        "density": 3.2,
        "category": "frameworks",
        "in_jd": true,
        "context_usage": [
          "Built React applications",
          "React component development"
        ]
      }
    ],
    "formatting_issues": [
      {
        "issue_type": "multi_column",
        "severity": "high",
        "description": "Resume uses two-column layout",
        "recommendation": "Convert to single-column for ATS parsing"
      }
    ],
    "semantic_similarity_score": 0.89
  },
  "optimized_cv": {
    "markdown": "# JOHN DOE\nFull Stack Developer\n\n## PROFESSIONAL SUMMARY\n...",
    "sections": {
      "sections": [],
      "total_sections": 0
    }
  },
  "parsed_resume": {
    "personalInfo": {
      "name": "John Doe",
      "title": "Full Stack Developer",
      "email": "john@example.com",
      "phone": "+1234567890",
      "location": "San Francisco, CA",
      "linkedin": "linkedin.com/in/johndoe"
    }
  }
}
```

**Errors:**
- `404`: Session not found
- `400`: Invalid job description
- `429`: Rate limit exceeded
- `500`: AI service error

**Example:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "9b229850-d7ee-4588-8d2d-f8f72a745d87",
    "job_description": "Full Stack Developer with React and Node.js experience..."
  }'
```

---

### 4. Download Optimized CV

#### `GET /api/download/{session_id}/markdown`
Download optimized CV in Markdown format.

**Parameters:**
- `session_id`: Session UUID

**Response:** `200 OK`
```
Content-Type: text/markdown
Content-Disposition: attachment; filename="resume_optimized.md"

# JOHN DOE
Full Stack Developer
...
```

**Example:**
```bash
curl -X GET http://localhost:8000/api/download/9b229850.../markdown \
  -o resume_optimized.md
```

---

#### `GET /api/download/{session_id}/pdf`
Download optimized CV in PDF format.

**Parameters:**
- `session_id`: Session UUID

**Response:** `200 OK`
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="resume_optimized.pdf"

[PDF Binary Data]
```

**Features:**
- Professional formatting
- ATS-friendly layout
- Clean typography
- Proper spacing and margins

**Example:**
```bash
curl -X GET http://localhost:8000/api/download/9b229850.../pdf \
  -o resume_optimized.pdf
```

---

#### `GET /api/download/{session_id}/docx`
Download optimized CV in DOCX format (ATS-optimized).

**Parameters:**
- `session_id`: Session UUID

**Response:** `200 OK`
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="resume_ATS_optimized.docx"

[DOCX Binary Data]
```

**Features:**
- Single-column layout
- ATS-safe fonts (Calibri, Arial, Times New Roman)
- Proper heading hierarchy
- No tables, text boxes, or graphics
- Standard margins (1 inch)
- Consistent formatting

**Example:**
```bash
curl -X GET http://localhost:8000/api/download/9b229850.../docx \
  -o resume_optimized.docx
```

---

### 5. Get Session Data

#### `GET /api/session/{session_id}`
Retrieve complete session data including analysis results.

**Parameters:**
- `session_id`: Session UUID

**Response:** `200 OK`
```json
{
  "session_id": "9b229850-d7ee-4588-8d2d-f8f72a745d87",
  "original_filename": "resume.pdf",
  "file_hash": "232ac6b7eb8ac9f4e7087a40cb214779...",
  "file_type": "pdf",
  "parsed_data": { ... },
  "analysis": { ... },
  "optimized_cv": { ... },
  "created_at": "2025-12-28T14:00:00Z",
  "updated_at": "2025-12-28T14:05:00Z"
}
```

**Errors:**
- `404`: Session not found

**Example:**
```bash
curl -X GET http://localhost:8000/api/session/9b229850-d7ee-4588-8d2d-f8f72a745d87
```

---

## Data Models

### CVSession (Database Model)

```python
{
  "_id": ObjectId,
  "session_id": str,              # UUID
  "original_filename": str,
  "file_hash": str,               # SHA-256
  "file_type": str,               # "pdf"
  "extracted_text": str,
  "parsed_data": ParsedCVData,
  "job_description": str | None,
  "analysis": dict | None,
  "optimized_cv": dict | None,
  "created_at": datetime,
  "updated_at": datetime
}
```

### ParsedCVData

```python
{
  "skills": List[str],
  "experience": List[WorkExperience],
  "education": List[Education],
  "contact": ContactInfo
}
```

### WorkExperience

```python
{
  "title": str,
  "company": str,
  "duration": str,
  "description": str,
  "start_date": str | None,
  "end_date": str | None
}
```

### Education

```python
{
  "degree": str,
  "institution": str,
  "year": str,
  "gpa": str | None,
  "honors": str | None
}
```

### ContactInfo

```python
{
  "name": str | None,
  "email": str | None,
  "phone": str | None,
  "linkedin": str | None,
  "location": str | None
}
```

---

## Error Handling

### Standard Error Response

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "details": { ... }  // Optional
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `413 Payload Too Large`: File exceeds size limit
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Common Errors

**File Upload Errors:**
```json
{
  "error": "Invalid file type",
  "message": "Only PDF files are accepted"
}
```

**Session Not Found:**
```json
{
  "error": "Session not found",
  "message": "Session ID 'xxx' does not exist or has expired"
}
```

**Rate Limit:**
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later."
}
```

---

## Security Features

### 1. File Validation

- **Type validation:** Only PDF files accepted
- **Magic number check:** Validates file signature
- **Size limit:** Maximum 10MB
- **PDF structure validation:** Checks for corrupted files
- **Quarantine system:** Suspicious files moved to quarantine

### 2. Rate Limiting

- Upload endpoint: 10 requests/minute
- Analyze endpoint: 5 requests/minute
- Download endpoints: 20 requests/minute

### 3. CORS Configuration

```python
# Development
ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]

# Production
ALLOWED_ORIGINS = ["https://yourdomain.com"]
```

### 4. Input Sanitization

- File hash verification (SHA-256)
- Pydantic schema validation
- SQL injection prevention (NoSQL)
- XSS prevention in text processing

### 5. Data Privacy

- Files stored with unique session IDs
- No permanent storage of uploaded files
- Session data expires after 24 hours
- Secure file deletion

---

## Testing

### Running Tests

```bash
# Setup test
python test_setup.py

# MongoDB connection test
python test_mongodb_detailed.py

# Manual API testing
# 1. Start server
python main.py

# 2. Run test suite
curl -X POST http://localhost:8000/api/upload -F "file=@test-resume.pdf"
# ... (see examples above)
```

### Test Results (Latest Run)

```
✅ All packages installed
✅ spaCy model loaded (en_core_web_md)
✅ Environment configured
✅ MongoDB connection successful
✅ OpenRouter API configured

API Endpoints Tested:
✅ GET / - Root endpoint
✅ GET /health - Health check
✅ POST /api/upload - File upload (145KB PDF)
✅ POST /api/analyze - CV analysis
   - Score: 88/100
   - ATS Compatibility: 95/100
   - Match: 92%
✅ GET /api/download/{id}/markdown - Downloaded (3.9KB)
✅ GET /api/download/{id}/pdf - Downloaded (26KB)
✅ GET /api/download/{id}/docx - Downloaded (36KB)
✅ GET /api/session/{id} - Retrieved session data
```

---

## Performance Metrics

- **Upload processing:** ~1-2 seconds
- **AI analysis:** ~5-10 seconds (depends on model)
- **PDF generation:** ~1-2 seconds
- **DOCX generation:** ~0.5-1 seconds
- **Database queries:** <100ms

---

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t cv-wizard-backend .

# Run container
docker run -p 8000:8000 --env-file .env cv-wizard-backend
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure production MongoDB URI
- [ ] Set secure `ALLOWED_ORIGINS`
- [ ] Use production OpenRouter model
- [ ] Enable HTTPS
- [ ] Set up monitoring (logs, metrics)
- [ ] Configure backup strategy
- [ ] Set up rate limiting
- [ ] Enable file upload scanning
- [ ] Configure CDN for file downloads

---

## Support & Contact

For issues or questions:
- GitHub Issues: https://github.com/yourusername/cv-wizard/issues
- Documentation: See `/docs` endpoint for interactive API docs

---

**Last Updated:** 2025-12-28  
**API Version:** 1.0.0
