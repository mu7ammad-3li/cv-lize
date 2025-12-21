"""
Download routes for optimized CVs
"""

import os
import tempfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from models.database import get_cv_session
from services.pdf_generator import pdf_generator

router = APIRouter(prefix="/api", tags=["download"])


@router.get("/download/{session_id}/markdown")
async def download_markdown(session_id: str):
    """
    Download optimized CV as Markdown file
    """
    # Fetch session
    session = await get_cv_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    # Get optimized CV
    optimized_cv = session.get("optimized_cv")
    if not optimized_cv or not optimized_cv.get("markdown"):
        raise HTTPException(
            status_code=404,
            detail="Optimized CV not found. Please analyze the CV first.",
        )

    markdown_content = optimized_cv["markdown"]

    # Get original filename (remove extension, add .md)
    original_filename = session.get("original_filename", "resume")
    base_name = os.path.splitext(original_filename)[0]
    filename = f"{base_name}_optimized.md"

    # Return as file download
    return Response(
        content=markdown_content.encode("utf-8"),
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/download/{session_id}/pdf")
async def download_pdf(session_id: str):
    """
    Download optimized CV as PDF file using WeasyPrint

    Generates a professional PDF with:
    - Structured sections from markdown parser
    - LinkedIn icon for LinkedIn profiles
    - Professional formatting and typography
    """
    # Fetch session
    session = await get_cv_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    # Get optimized CV and parsed resume data
    optimized_cv = session.get("optimized_cv")
    if not optimized_cv:
        raise HTTPException(
            status_code=404,
            detail="Optimized CV not found. Please analyze the CV first.",
        )

    # Get parsed resume data (for personal info and fallback data)
    parsed_resume = session.get("parsed_resume")
    if not parsed_resume:
        raise HTTPException(
            status_code=400,
            detail="Resume data not parsed. Please re-analyze the CV.",
        )

    try:
        # Get structured sections if available
        sections = optimized_cv.get("sections")

        # Generate PDF using the structured template
        pdf_bytes = pdf_generator.generate_from_parsed_resume(
            parsed_resume=parsed_resume, sections=sections
        )

        # Get original filename (remove extension, add .pdf)
        original_filename = session.get("original_filename", "resume")
        base_name = os.path.splitext(original_filename)[0]
        filename = f"{base_name}_optimized.pdf"

        print(f"✅ Generated PDF for session {session_id}: {filename}")
        print(f"   Used structured sections: {bool(sections)}")

        # Return PDF as download
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf",
            },
        )

    except Exception as e:
        print(f"❌ PDF generation failed for session {session_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}",
        )


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get session data
    """
    session = await get_cv_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    # Remove sensitive data
    session.pop("_id", None)
    session.pop("extracted_text", None)  # Too large for response

    return session
