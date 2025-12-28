# RenderCV Installation & Testing Guide

## Quick Start

### 1. Install RenderCV

```bash
cd /media/muhammad/Work/Identity/CV-lize/backend
pip install "rendercv[full]==2.5"
```

Or if using a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
rendercv --version
```

Should output: `RenderCV v2.5`

### 3. Test the Migration

Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

Upload a resume through the API or frontend, then test PDF generation:

```bash
# Replace {session_id} with actual session ID

# Test RenderCV (default)
curl -o test_rendercv.pdf "http://localhost:8000/api/download/{session_id}/pdf"

# Test specific theme
curl -o test_classic.pdf "http://localhost:8000/api/download/{session_id}/pdf?theme=classic"

# Test WeasyPrint fallback
curl -o test_weasy.pdf "http://localhost:8000/api/download/{session_id}/pdf?engine=weasyprint"
```

## Available Themes

1. **engineeringresumes** (default) - Clean, ATS-friendly
2. **engineeringclassic** - Professional with colors
3. **classic** - Traditional academic
4. **sb2nov** - Minimalist two-column
5. **moderncv** - Modern with sidebar

## Supported Fonts

- Arial (default)
- Calibri
- Helvetica
- Times New Roman
- Georgia
- Garamond
- Raleway
- Open Sans
- Lato
- Source Sans 3

## Troubleshooting

### RenderCV Not Found

If you see `ImportError: RenderCV is not installed`:

```bash
pip install "rendercv[full]==2.5"
```

### System Reports External Environment

If pip refuses to install (externally-managed-environment):

```bash
# Option 1: Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install "rendercv[full]==2.5"

# Option 2: User install
pip install --user "rendercv[full]==2.5"
```

### Typst Not Found

RenderCV requires Typst. If missing:

```bash
# Install via rendercv[full]
pip install "rendercv[full]==2.5"
```

The `[full]` extra includes all dependencies including Typst.

## What to Expect

### Success Indicators ✅

**RenderCV Generation:**
```
🎨 Generating PDF with RenderCV (theme: engineeringresumes)
✅ Generated PDF for session abc123: resume_optimized.pdf
   Engine: rendercv
   Theme: engineeringresumes
   Font: Arial
```

**WeasyPrint Fallback:**
```
📄 Generating PDF with WeasyPrint (PDF/A-3u for ATS compliance)
📋 Generating PDF with variant: pdf/a-3u for enhanced ATS compatibility
✅ Generated PDF for session abc123: resume_optimized.pdf
   Engine: weasyprint
```

**Automatic Fallback:**
```
⚠️  RenderCV not installed, falling back to WeasyPrint
📄 Generating PDF with WeasyPrint (PDF/A-3u for ATS compliance)
```

## Next Steps

1. Test with your own resume
2. Try different themes and compare output
3. Verify ATS compatibility
4. Update frontend to add theme selector

## Support

Check `RENDERCV_MIGRATION.md` for detailed migration information.
