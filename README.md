<div align="center">

# 📄 CV-lize

### AI-Powered Resume Optimization Platform

Transform your resume with cutting-edge AI technology. Get instant analysis, ATS compatibility checks, and professionally optimized resumes tailored to your target job.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19.2-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)

[Live Demo](https://cv-lize.vercel.app) · [Report Bug](https://github.com/mu7ammad-3li/cv-lize/issues) · [Request Feature](https://github.com/mu7ammad-3li/cv-lize/issues)

![CV-lize Screenshot](./docs/images/screenshot.png)

</div>

---

## 📑 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#%EF%B8%8F-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Security](#-security)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- **Multi-Format Support**: Upload CVs in PDF, Markdown, or Text
- **AI-Powered Analysis**: Powered by Google Gemini & OpenRouter
- **ATS Optimization**: 95%+ ATS compatibility score
- **Real-time Preview**: Professional resume template with live preview
- **Instant Results**: Get optimized CV in under 30 seconds
- **Export Options**: Download as Markdown or PDF

</td>
<td width="50%">

### 🔒 Security & Performance
- **Multi-Layer Validation**: Advanced security scanning
- **Malware Detection**: Reverse shell & malicious content detection
- **Rate Limiting**: 50 requests/hour protection
- **Anonymous Usage**: No sign-up required
- **Data Privacy**: 24-hour auto-deletion
- **File Quarantine**: Suspicious files isolated

</td>
</tr>
</table>

---

## 🎬 Demo

### Upload Interface
Upload your CV and optionally paste a job description for tailored optimization.

![Upload Interface](./docs/images/screenshot.png)

### Key Capabilities

- **📤 Drag & Drop Upload**: Easy file upload with support for PDF, Markdown, and Text
- **🤖 AI Analysis**: Comprehensive CV analysis with actionable insights
- **📊 ATS Scoring**: Detailed compatibility metrics for Applicant Tracking Systems
- **✨ Professional Templates**: Clean, ATS-friendly resume designs
- **🎨 Live Preview**: Real-time preview of optimized resume
- **💾 Multiple Formats**: Download as Markdown or PDF

---

## 🏗️ Architecture

```mermaid
graph TB
    A[User] -->|Upload CV| B[Frontend - React + Vite]
    B -->|API Request| C[Backend - FastAPI]
    C -->|Store| D[MongoDB Atlas]
    C -->|Analyze| E[spaCy NLP]
    C -->|Optimize| F[AI - Gemini/OpenRouter]
    C -->|Validate| G[Security Scanner]
    F -->|Optimized CV| C
    C -->|Response| B
    B -->|Display| A
```

### Components

**Frontend (React + TypeScript + Vite)**
- Modern React 19 with TypeScript for type safety
- Vite for lightning-fast development and builds
- TailwindCSS for responsive, utility-first styling
- shadcn/ui for beautiful, accessible components
- Framer Motion for smooth animations

**Backend (FastAPI + Python)**
- Async FastAPI for high-performance API
- spaCy for advanced NLP and entity extraction
- MongoDB Atlas for scalable cloud database
- Multi-AI support (Gemini & OpenRouter)
- WeasyPrint for server-side PDF generation

---

## 🛠 Tech Stack

<div align="center">

### Frontend
![React](https://img.shields.io/badge/React-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7.2-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-4.1-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

### AI & ML
![Google](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)

</div>

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **MongoDB Atlas Account** ([Sign Up](https://www.mongodb.com/cloud/atlas) - Free M0 tier)
- **OpenRouter API Key** ([Get Key](https://openrouter.ai/) - Free tier available)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/mu7ammad-3li/cv-lize.git
cd cv-lize/backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

5. **Configure environment variables**

Create `.env` file in `backend/` directory:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/cvlize?retryWrites=true&w=majority

# OpenRouter AI
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Google Gemini (Optional - alternative to OpenRouter)
GEMINI_API_KEY=your-gemini-api-key

# Application
ENVIRONMENT=development
DEBUG=True
PORT=8000
HOST=0.0.0.0

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# File Upload
MAX_FILE_SIZE=5242880
UPLOAD_DIR=./uploads
QUARANTINE_DIR=./quarantine

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_WINDOW=900

# Session
SESSION_TTL_HOURS=24
```

6. **Run the backend server**
```bash
# Development
python main.py

# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment** (optional)

Create `.env` file in `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

4. **Run development server**
```bash
npm run dev
```

Frontend will be running at: **http://localhost:5173**

5. **Build for production**
```bash
npm run build
```

---

## 📁 Project Structure

```
cv-lize/
├── 📂 backend/                      # FastAPI Backend
│   ├── main.py                      # Application entry point
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables (create this)
│   ├── .env.example                 # Environment template
│   ├── Dockerfile                   # Docker configuration
│   ├── 📂 routes/                   # API endpoints
│   │   ├── upload.py               # CV upload endpoint
│   │   ├── analyze.py              # AI analysis endpoint
│   │   └── download.py             # Download endpoints
│   ├── 📂 services/                 # Business logic
│   │   ├── nlp_processor.py        # spaCy CV parsing
│   │   ├── gemini_service.py       # Google Gemini AI
│   │   ├── openrouter_service.py   # OpenRouter AI
│   │   ├── markdown_parser.py      # Markdown processing
│   │   └── pdf_generator.py        # PDF generation
│   ├── 📂 models/                   # Data models
│   │   ├── schemas.py              # Pydantic schemas
│   │   └── database.py             # MongoDB connection
│   ├── 📂 middleware/               # Middleware
│   │   └── rate_limit.py           # Rate limiting
│   ├── 📂 utils/                    # Utilities
│   │   └── pdf_validator.py        # Security validation
│   └── 📂 templates/                # PDF templates
│       ├── professional.html        # Professional template
│       └── professional_structured_v2.html  # ATS-optimized template
├── 📂 frontend/                     # React Frontend
│   ├── 📂 src/
│   │   ├── App.tsx                 # Main application
│   │   ├── main.tsx                # Entry point
│   │   ├── index.css               # Global styles
│   │   ├── 📂 components/          # React components
│   │   │   ├── HomePage.tsx        # Landing page
│   │   │   ├── FileUpload.tsx      # Drag-drop upload
│   │   │   ├── CVAnalysis.tsx      # Analysis display
│   │   │   ├── ProfessionalTemplate.tsx  # Resume template
│   │   │   └── 📂 ui/              # shadcn/ui components
│   │   ├── 📂 lib/                 # Utilities
│   │   │   ├── api.ts              # API client
│   │   │   └── utils.ts            # Helper functions
│   │   └── 📂 templates/           # Additional templates
│   ├── package.json                # Node dependencies
│   ├── vite.config.ts              # Vite configuration
│   ├── tailwind.config.js          # Tailwind configuration
│   └── tsconfig.json               # TypeScript configuration
├── 📂 docs/                        # Documentation
│   ├── 📂 images/                  # Screenshots & images
│   │   └── screenshot.png
│   ├── API.md                      # API documentation
│   ├── DEPLOYMENT.md               # Deployment guides
│   ├── FREE_DEPLOYMENT.md          # Free deployment options
│   └── AWS_DEPLOYMENT.md           # AWS deployment guide
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── LICENSE                         # MIT License
└── GITIGNORE_GUIDE.md             # Gitignore documentation
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Upload CV
```http
POST /api/upload
Content-Type: multipart/form-data

Parameters:
- file: File (PDF, Markdown, or Text)

Response: 200 OK
{
  "session_id": "uuid-v4",
  "filename": "john_doe_cv.pdf",
  "file_hash": "sha256...",
  "file_type": "pdf",
  "extracted_text": "...",
  "parsed_data": {
    "skills": ["Python", "FastAPI", "React"],
    "experience": [...],
    "education": [...],
    "contact": {...}
  }
}
```

#### 2. Analyze CV
```http
POST /api/analyze
Content-Type: application/json

Body:
{
  "session_id": "uuid-v4",
  "job_description": "We are seeking a Full Stack Developer..."
}

Response: 200 OK
{
  "analysis": {
    "score": 85,
    "ats_compatibility": 92,
    "match_percentage": 78,
    "strengths": ["Strong technical skills", ...],
    "weaknesses": ["Limited management experience", ...],
    "suggestions": ["Add cloud certifications", ...]
  },
  "optimized_cv": {
    "markdown": "# Full Name\n\n## Professional Summary\n..."
  },
  "parsed_resume": {
    "personalInfo": {...},
    "sections": [...]
  }
}
```

#### 3. Download Optimized CV
```http
GET /api/download/{session_id}/markdown
GET /api/download/{session_id}/pdf

Response: File download
```

#### 4. Health Check
```http
GET /health

Response: 200 OK
{
  "status": "healthy",
  "database": "connected"
}
```

### Interactive API Docs
Visit **http://localhost:8000/docs** for Swagger UI interactive documentation.

---

## 🔒 Security

CV-lize implements enterprise-grade security measures:

### File Validation
✅ **Magic Byte Verification** - Validates actual file type  
✅ **Size Limits** - Maximum 5MB per file  
✅ **Format Validation** - Only PDF, Markdown, and Text allowed

### Malware Detection
✅ **Embedded JavaScript** - Detects XSS attempts  
✅ **Executable Files** - Blocks PE/ELF/Mach-O binaries  
✅ **Remote File Redirects** - Prevents SMB attacks  
✅ **XFA Forms** - Detects XXE vulnerabilities  

### Reverse Shell Detection
✅ **Bash Reverse Shells** - `bash -i >& /dev/tcp/`  
✅ **Python Sockets** - `socket.socket()`  
✅ **Netcat/Socat** - Common backdoor patterns  
✅ **PowerShell TCP** - `System.Net.Sockets.TCPClient`  
✅ **Ruby/Perl Shells** - Various reverse shell patterns

### Application Security
✅ **Rate Limiting** - 50 requests/hour per IP  
✅ **CORS Protection** - Whitelist-based origins  
✅ **Input Sanitization** - All user inputs sanitized  
✅ **Session Management** - 24-hour TTL with auto-cleanup  
✅ **File Quarantine** - Suspicious files isolated with SHA-256 logging

---

## 🌐 Deployment

### Quick Deployment Options

<table>
<tr>
<td width="33%">

#### Vercel (Frontend)
```bash
cd frontend
vercel
```
[Deploy Guide](./docs/FREE_DEPLOYMENT.md)

</td>
<td width="33%">

#### Render (Backend)
```bash
cd backend
# Connect GitHub repo
```
[Deploy Guide](./docs/FREE_DEPLOYMENT.md)

</td>
<td width="33%">

#### AWS (Full Stack)
```bash
# See AWS guide
```
[Deploy Guide](./docs/AWS_DEPLOYMENT.md)

</td>
</tr>
</table>

### Environment Variables (Production)

**Backend:**
```env
MONGODB_URI=mongodb+srv://...
OPENROUTER_API_KEY=sk-or-v1-...
ALLOWED_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
DEBUG=False
```

**Frontend:**
```env
VITE_API_URL=https://your-backend.render.com
```

For detailed deployment instructions, see:
- [Free Deployment Guide](./docs/FREE_DEPLOYMENT.md) - Vercel + Render (100% Free)
- [AWS Deployment Guide](./docs/AWS_DEPLOYMENT.md) - AWS Free Tier
- [General Deployment](./docs/DEPLOYMENT.md) - All options

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow existing code style
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

### Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📧 Contact

**Muhammad Ali**

- GitHub: [@mu7ammad-3li](https://github.com/mu7ammad-3li/)
- Email: muhammad.3lii2@gmail.com
- LinkedIn: [linkedin.com/in/muhammad-3lii](https://linkedin.com/in/muhammad-3lii)

**Project Link**: [https://github.com/mu7ammad-3li/cv-lize](https://github.com/mu7ammad-3li/cv-lize)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful component library
- [spaCy](https://spacy.io/) - Advanced NLP
- [Google Gemini](https://ai.google.dev/) - AI analysis
- [OpenRouter](https://openrouter.ai/) - AI gateway
- [MongoDB Atlas](https://www.mongodb.com/atlas) - Cloud database
- [Vercel](https://vercel.com/) - Frontend deployment
- [Render](https://render.com/) - Backend deployment

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=mu7ammad-3li/cv-lize&type=Date)](https://star-history.com/#mu7ammad-3li/cv-lize&Date)

---

<div align="center">

**Built with ❤️ by [Muhammad Ali](https://github.com/mu7ammad-3li/)**

[⬆ Back to Top](#-cv-lize)

</div>
