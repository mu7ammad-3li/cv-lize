# Changelog

All notable changes to the CV Wizard project will be documented in this file.

## [1.0.0] - 2024-12-20

### 🎉 Initial Release

#### Added - Backend

**AI Integration**
- Integrated OpenRouter AI with NVIDIA Nemotron 3 Nano 30B A3B model
- Replaced Google Gemini with OpenRouter for better flexibility and free tier access
- Configured 256K context window support
- Set input limits: 10K characters (CV), 5K characters (Job Description)
- Set output limit: 16K tokens for comprehensive CV generation

**API Endpoints**
- `POST /api/upload` - CV file upload with security validation
- `POST /api/analyze` - AI-powered CV analysis against job description
- `GET /api/download/{session_id}/markdown` - Download optimized CV as markdown
- `GET /api/session/{session_id}` - Retrieve session data

**Security Features**
- Multi-layer PDF validation (magic bytes, embedded content)
- Reverse shell pattern detection
- Malicious content scanning
- File size limits (5MB max)
- Rate limiting: 50 requests per hour
- File quarantine system with SHA-256 hash logging

**Database**
- MongoDB Atlas integration with Motor (async driver)
- Session management with 24-hour TTL
- Automatic index creation for performance
- Optimized queries for fast retrieval

**NLP Processing**
- spaCy en_core_web_md model integration
- Entity extraction: skills, experience, education, contact info
- Pattern matching for job titles, dates, companies

**Configuration**
- Environment-based configuration
- CORS support for frontend integration
- Debug mode for development
- Comprehensive error handling and logging

#### Added - Frontend

**Core Features**
- React 19 application with TypeScript
- Vite 7 build system for fast development
- TailwindCSS 4 for styling
- shadcn/ui component library integration

**Components**
- `FileUpload.tsx` - Drag-and-drop file upload with preview
- `CVAnalysis.tsx` - Analysis results display with dual view modes
- `ProfessionalResumeDisplay.tsx` - Multi-page professional resume template
- UI components: Button, Card, Separator (shadcn/ui)

**Professional Resume Template**
- Clean, ATS-friendly design
- Multi-page support with proper page breaks
- A4 page size (210mm x 297mm)
- Print-optimized styles
- Sections: Header, Professional Summary, Experience, Skills, Education, Certifications
- No images or decorative elements
- Framer Motion animations

**View Modes**
- Professional View: Beautiful resume template with structured layout
- Markdown View: Raw markdown preview
- Toggle between views with button controls

**Features**
- Real-time CV analysis with loading states
- Error handling with user-friendly messages
- Print-to-PDF functionality via browser print dialog
- Download optimized CV as markdown
- Responsive design for mobile and desktop
- Session-based workflow (no login required)

**API Integration**
- Axios client with proxy configuration
- TypeScript interfaces for type safety
- Error handling and retry logic
- Progress indicators for long-running operations

**Markdown Parser**
- Custom parser to convert AI-generated markdown to structured data
- Extracts: name, title, summary, contact info, experience, skills, education, certifications
- Handles various markdown formats
- Regex-based pattern matching

### Technical Details

**Backend Stack**
- FastAPI 0.104.1
- Motor 3.3.2 (MongoDB async driver)
- spaCy 3.8.2
- OpenAI SDK 2.14.0 (OpenRouter compatible)
- pdfplumber 0.10.3
- SlowAPI 0.1.9 (rate limiting)
- python-dotenv 1.0.0

**Frontend Stack**
- React 19.2.0
- TypeScript 5.9.3
- Vite 7.2.4
- TailwindCSS 4.1.18
- shadcn/ui components
- Framer Motion (animations)
- react-markdown 10.1.0
- Axios 1.13.2

**AI Model**
- Provider: OpenRouter AI
- Model: NVIDIA Nemotron 3 Nano 30B A3B
- Tier: Free
- Context: 256K tokens
- Latency: 0.29s average
- Throughput: 403.7 tokens/second

### Configuration Changes

**Backend Environment Variables**
```env
MONGODB_URI - MongoDB Atlas connection string
OPENROUTER_API_KEY - OpenRouter API key
OPENROUTER_MODEL - AI model identifier
ENVIRONMENT - development/production
DEBUG - True/False
PORT - Server port (default: 8000)
HOST - Server host (default: 0.0.0.0)
MAX_FILE_SIZE - Max upload size (default: 5MB)
UPLOAD_DIR - Upload directory
QUARANTINE_DIR - Quarantine directory
RATE_LIMIT_PER_MINUTE - Rate limit count
RATE_LIMIT_WINDOW - Rate limit window (seconds)
SESSION_TTL_HOURS - Session expiry (default: 24)
```

**Frontend Configuration**
- Vite proxy: `/api` → `http://localhost:8000`
- TypeScript path aliases: `@/*` → `./src/*`
- TailwindCSS 4 with custom theme
- Import aliases for components

### Security Enhancements

**Implemented Protections**
- PDF magic byte validation
- JavaScript detection in PDFs
- Executable detection in PDFs
- Remote file redirect detection
- XFA form detection (XXE prevention)
- Reverse shell pattern detection (15+ patterns)
- Rate limiting per IP address
- File hash verification (SHA-256)
- Automatic file quarantine

**Patterns Detected**
- Bash reverse shells
- Python socket connections
- Netcat/Socat backdoors
- PowerShell TCP clients
- Ruby reverse shells
- Perl reverse shells
- PHP reverse shells
- And more...

### Known Issues

1. **PDF Generation**: Backend PDF generation endpoint not yet implemented. Users can use browser print dialog as workaround.

2. **Token Truncation**: CVs longer than 10K characters are truncated before analysis. Solution: Implement chunking strategy.

3. **Markdown Parsing**: Parser may miss some edge cases in unusual CV formats. Solution: Continuous improvement based on real-world CVs.

4. **Mobile Experience**: Professional resume view optimized for desktop/print. Mobile view needs refinement.

### Performance Metrics

**Backend**
- Average response time: ~2-3 seconds for analysis
- Memory usage: ~150MB (with spaCy model loaded)
- PDF processing: ~500ms per page
- Rate limit: 50 requests/hour per IP

**Frontend**
- Initial load: ~200ms
- Bundle size: ~500KB (gzipped)
- Time to Interactive: ~1s
- Lighthouse Score: 90+ (Performance)

### Migration Notes

**From Gemini to OpenRouter**
1. Replaced `google.generativeai` with OpenAI SDK
2. Updated service file: `gemini_service.py` → `openrouter_service.py`
3. Changed API endpoint and authentication
4. Updated prompt format for OpenAI-compatible API
5. Increased token limits (4K → 16K output)
6. Updated environment variables
7. Modified test setup to check OpenRouter instead of Gemini

### Future Roadmap

**Version 1.1 (Planned)**
- Backend PDF generation with WeasyPrint
- Multiple resume templates (Modern, Minimal, Creative)
- Cover letter generation
- Batch CV processing

**Version 1.2 (Planned)**
- User accounts (optional)
- CV history and versioning
- Interview question preparation
- LinkedIn profile optimization

**Version 2.0 (Future)**
- Multi-language support
- Video resume analysis
- AI-powered job matching
- Analytics dashboard

---

**Release Date**: December 20, 2024  
**Contributors**: Muhammad Ali Alsayed  
**License**: MIT
