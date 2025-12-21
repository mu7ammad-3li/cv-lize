"""
Upload route for CV files
"""

import os
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from middleware.rate_limit import limiter
from models.database import check_duplicate_file, create_cv_session
from models.schemas import FileType, UploadResponse
from services.nlp_processor import cv_parser
from utils.file_handler import (
    calculate_file_hash,
    extract_text_from_markdown,
    extract_text_from_pdf,
    extract_text_from_txt,
    get_file_type,
    save_quarantined_file,
)
from utils.pdf_validator import pdf_validator

router = APIRouter(prefix="/api", tags=["upload"])

# Maximum file size (5MB)
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5242880))


@router.post("/upload", response_model=UploadResponse)
@limiter.limit("10/15minutes")  # 10 uploads per 15 minutes
async def upload_cv(request: Request, file: UploadFile = File(...)):
    """
    Upload and process CV file (PDF, Markdown, or Text)

    Steps:
    1. Validate file size and type
    2. Security scan (for PDFs)
    3. Extract text
    4. Parse entities with spaCy
    5. Store in MongoDB
    6. Return session data
    """

    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024:.1f}MB",
        )

    # Determine file type
    try:
        file_type = get_file_type(str(file.filename))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Calculate file hash
    file_hash = calculate_file_hash(content)

    # Check for duplicate file
    existing_session = await check_duplicate_file(file_hash)
    if existing_session:
        # Return existing session data
        return UploadResponse(
            session_id=existing_session["session_id"],
            filename=existing_session["original_filename"],
            file_hash=file_hash,
            extracted_text=existing_session["extracted_text"][:500] + "...",
            parsed_data=existing_session.get("parsed_data", {}),
        )

    # PDF security validation
    if file_type == "pdf":
        is_valid, issues, _ = pdf_validator.validate(content)

        if not is_valid:
            # Quarantine suspicious file
            quarantine_path = await save_quarantined_file(
                content, str(file.filename), file_hash
            )

            # Log security event
            print(f"🚨 SECURITY: Quarantined file {file.filename} to {quarantine_path}")
            print(f"   Issues: {issues}")

            # Return security error
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Security validation failed",
                    "message": "File contains potentially malicious content",
                    "issues": issues,
                    "risk_level": pdf_validator.get_risk_level(issues),
                },
            )

    # Extract text based on file type
    try:
        if file_type == "pdf":
            extracted_text = await extract_text_from_pdf(content)
        elif file_type == "markdown":
            extracted_text = await extract_text_from_markdown(content)
        else:  # txt
            extracted_text = await extract_text_from_txt(content)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to extract text from file: {str(e)}"
        )

    # Validate extracted text
    if not extracted_text or len(extracted_text) < 50:
        raise HTTPException(
            status_code=400,
            detail="Extracted text is too short. Please ensure the file contains a valid CV.",
        )

    # Parse CV entities with spaCy
    try:
        parsed_data = await cv_parser.extract_cv_entities(extracted_text)
    except Exception as e:
        print(f"⚠️  Warning: spaCy parsing failed: {e}")
        # Continue without parsed data
        parsed_data = None

    # Generate session ID
    session_id = str(uuid.uuid4())

    # Create session in database
    session_data = {
        "session_id": session_id,
        "original_filename": file.filename,
        "file_hash": file_hash,
        "file_type": file_type,
        "extracted_text": extracted_text,
        "parsed_data": parsed_data.dict() if parsed_data else None,
        "job_description": None,
        "analysis": None,
        "optimized_cv": None,
    }

    await create_cv_session(session_data)

    print(f"✅ Created session {session_id} for {file.filename}")

    # Return response
    return UploadResponse(
        session_id=session_id,
        filename=file.filename,
        file_hash=file_hash,
        extracted_text=extracted_text[:500] + "..."
        if len(extracted_text) > 500
        else extracted_text,
        parsed_data=parsed_data if parsed_data else {},
    )
