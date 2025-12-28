"""
Download routes for optimized CVs
"""

import os
import tempfile
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, Response

from models.database import get_cv_session
from services.docx_generator import docx_generator
from services.pdf_generator import pdf_generator
from services.rendercv_generator import rendercv_generator
from services.section_filter import section_filter

router = APIRouter(prefix="/api", tags=["download"])


@router.get("/download/{session_id}/markdown")
async def download_markdown(
    session_id: str,
    sections: Optional[List[str]] = Query(None, description="Sections to include"),
):
    """
    Download optimized CV as Markdown file

    Query params:
        sections: List of section names to include (e.g., ?sections=Professional Summary&sections=Work Experience)
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

    # Filter sections if specified
    if sections:
        markdown_content = section_filter.filter_markdown_sections(
            markdown_content, set(sections)
        )

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
async def download_pdf(
    session_id: str,
    sections: Optional[List[str]] = Query(None, description="Sections to include"),
    font: Optional[str] = Query("Arial", description="Font family for the resume"),
    engine: Optional[str] = Query(
        "rendercv", description="PDF rendering engine: 'rendercv' or 'weasyprint'"
    ),
    theme: Optional[str] = Query(
        "engineeringresumes", description="RenderCV theme (only for rendercv engine)"
    ),
):
    """
    Download optimized CV as PDF file

    PDF Generation Engines:
    - rendercv (default): Professional CV generation with Typst (superior typography)
    - weasyprint: HTML-based PDF generation (legacy option)

    RenderCV Themes (when engine=rendercv):
    - engineeringresumes: Clean, ATS-friendly for tech roles
    - engineeringclassic: Professional with color accents
    - classic: Traditional academic style
    - sb2nov: Minimalist two-column
    - moderncv: Modern with sidebar

    Query params:
        sections: List of section names to include
        font: Font family (Arial, Calibri, etc.)
        engine: PDF engine ('rendercv' or 'weasyprint')
        theme: RenderCV theme name
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

    # Filter markdown if sections specified
    markdown_content = optimized_cv.get("markdown", "")
    if sections and markdown_content:
        markdown_content = section_filter.filter_markdown_sections(
            markdown_content, set(sections)
        )
        # Update optimized_cv with filtered content
        optimized_cv = {**optimized_cv, "markdown": markdown_content}

        # Parse the filtered markdown to create new sections structure
        from services.markdown_parser import markdown_parser

        parsed_sections = markdown_parser.parse_sections(markdown_content)
        cv_sections = parsed_sections if parsed_sections else None
    else:
        # Use original sections if no filtering
        cv_sections = optimized_cv.get("sections")

    try:
        # Choose PDF generation engine
        if engine == "rendercv":
            # Use RenderCV for professional typography
            print(f"🎨 Generating PDF with RenderCV (theme: {theme})")
            pdf_bytes = rendercv_generator.generate_from_parsed_resume(
                parsed_resume=parsed_resume,
                sections=cv_sections,
                font_family=font,
                theme=theme,
            )
            engine_suffix = f"_rendercv_{theme}"
        else:
            # Use WeasyPrint (legacy HTML-based) with PDF/A-3u for ATS compliance
            print(f"📄 Generating PDF with WeasyPrint (PDF/A-3u for ATS compliance)")
            pdf_bytes = pdf_generator.generate_from_parsed_resume(
                parsed_resume=parsed_resume,
                sections=cv_sections,
                font_family=font,
                pdf_variant="pdf/a-3u",  # Enhanced ATS compatibility
            )
            engine_suffix = "_weasyprint"

        # Get original filename (remove extension, add .pdf)
        original_filename = session.get("original_filename", "resume")
        base_name = os.path.splitext(original_filename)[0]
        filename = f"{base_name}_optimized.pdf"

        print(f"✅ Generated PDF for session {session_id}: {filename}")
        print(f"   Engine: {engine}")
        print(f"   Theme: {theme if engine == 'rendercv' else 'N/A'}")
        print(f"   Font: {font}")
        print(f"   Used structured sections: {bool(cv_sections)}")
        print(f"   Sections filtered: {bool(sections)}")

        # Return PDF as download
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf",
            },
        )

    except ImportError as e:
        print(f"⚠️  RenderCV not installed, falling back to WeasyPrint")
        # Fallback to WeasyPrint if RenderCV not available
        try:
            pdf_bytes = pdf_generator.generate_from_parsed_resume(
                parsed_resume=parsed_resume, sections=cv_sections, font_family=font
            )

            original_filename = session.get("original_filename", "resume")
            base_name = os.path.splitext(original_filename)[0]
            filename = f"{base_name}_optimized.pdf"

            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}",
                    "Content-Type": "application/pdf",
                },
            )
        except Exception as fallback_error:
            raise HTTPException(
                status_code=500,
                detail=f"PDF generation failed: {str(fallback_error)}",
            )

    except Exception as e:
        print(f"❌ PDF generation failed for session {session_id}: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}",
        )


@router.get("/download/{session_id}/docx")
async def download_docx(
    session_id: str,
    sections: Optional[List[str]] = Query(None, description="Sections to include"),
    font: Optional[str] = Query("Calibri", description="Font family for the resume"),
):
    """
    Download optimized CV as DOCX file (ATS-optimized format)

    DOCX is the preferred format for ATS systems:
    - Single-column linear layout
    - Standard fonts (Calibri)
    - 1-inch margins
    - Left-aligned text
    - Contact info in main body (NOT header)
    - Standard section headers

    Query params:
        sections: List of section names to include
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

    # Get parsed resume data
    parsed_resume = session.get("parsed_resume")

    # Filter markdown if sections specified
    markdown_content = optimized_cv.get("markdown", "")
    if sections and markdown_content:
        markdown_content = section_filter.filter_markdown_sections(
            markdown_content, set(sections)
        )

    try:
        # Create generator with selected font
        from services.docx_generator import DOCXGenerator

        generator = DOCXGenerator(font_family=font)

        # Always use filtered markdown if sections are specified
        if sections and markdown_content:
            # Use filtered markdown for generation
            docx_bytes = generator.generate_from_markdown(markdown_content, None)
        elif parsed_resume:
            # Use parsed resume data if no filtering needed
            from models.schemas import ParsedResumeData

            resume_data = ParsedResumeData(**parsed_resume)
            docx_bytes = generator.generate_from_parsed_resume(resume_data)
        else:
            # Fallback to markdown conversion
            markdown_content = optimized_cv.get("markdown", "")
            if not markdown_content:
                raise HTTPException(
                    status_code=400,
                    detail="No resume content available for DOCX generation",
                )
            docx_bytes = generator.generate_from_markdown(markdown_content, None)

        # Get original filename (remove extension, add .docx)
        original_filename = session.get("original_filename", "resume")
        base_name = os.path.splitext(original_filename)[0]
        filename = f"{base_name}_ATS_optimized.docx"

        print(f"✅ Generated DOCX for session {session_id}: {filename}")

        # Return DOCX as download
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            },
        )

    except Exception as e:
        print(f"❌ DOCX generation failed for session {session_id}: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate DOCX: {str(e)}",
        )


@router.get("/download/{session_id}/plaintext")
async def download_plaintext(session_id: str):
    """
    Download plain text preview of resume

    This simulates the "Notepad Test" to show what an ATS parser sees
    after stripping all formatting. Useful for validation.
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

    # Strip markdown formatting to create plain text
    markdown_content = optimized_cv["markdown"]

    # Basic markdown stripping (remove #, *, **, etc.)
    import re

    plain_text = markdown_content
    plain_text = re.sub(
        r"^#{1,6}\s+", "", plain_text, flags=re.MULTILINE
    )  # Remove headers
    plain_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", plain_text)  # Remove bold
    plain_text = re.sub(r"\*([^*]+)\*", r"\1", plain_text)  # Remove italic
    plain_text = re.sub(
        r"^\s*[-*+]\s+", "• ", plain_text, flags=re.MULTILINE
    )  # Normalize bullets

    # Get original filename
    original_filename = session.get("original_filename", "resume")
    base_name = os.path.splitext(original_filename)[0]
    filename = f"{base_name}_plaintext_preview.txt"

    print(f"✅ Generated plain text preview for session {session_id}")

    # Return as plain text file
    return Response(
        content=plain_text.encode("utf-8"),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
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
