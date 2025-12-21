"""
File handling utilities for PDF, Markdown, and text files
"""

import hashlib
import os
from io import BytesIO
from typing import Tuple

import pdfplumber


async def extract_text_from_pdf(content: bytes) -> str:
    """
    Extract text from PDF file

    Args:
        content: PDF file content as bytes

    Returns:
        Extracted text
    """
    try:
        with pdfplumber.open(BytesIO(content)) as pdf:
            text_parts = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

            full_text = "\n\n".join(text_parts)
            return full_text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


async def extract_text_from_markdown(content: bytes) -> str:
    """
    Extract text from Markdown file

    Args:
        content: Markdown file content as bytes

    Returns:
        Text content
    """
    try:
        text = content.decode("utf-8")
        return text.strip()
    except UnicodeDecodeError:
        # Try other encodings
        try:
            text = content.decode("latin-1")
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to decode markdown file: {str(e)}")


async def extract_text_from_txt(content: bytes) -> str:
    """
    Extract text from plain text file

    Args:
        content: Text file content as bytes

    Returns:
        Text content
    """
    try:
        text = content.decode("utf-8")
        return text.strip()
    except UnicodeDecodeError:
        # Try other encodings
        encodings = ["latin-1", "cp1252", "iso-8859-1"]
        for encoding in encodings:
            try:
                text = content.decode(encoding)
                return text.strip()
            except UnicodeDecodeError:
                continue

        raise ValueError("Failed to decode text file with common encodings")


def calculate_file_hash(content: bytes) -> str:
    """
    Calculate SHA-256 hash of file content

    Args:
        content: File content as bytes

    Returns:
        Hex digest of SHA-256 hash
    """
    return hashlib.sha256(content).hexdigest()


async def save_quarantined_file(content: bytes, filename: str, file_hash: str) -> str:
    """
    Save suspicious file to quarantine directory

    Args:
        content: File content
        filename: Original filename
        file_hash: File hash

    Returns:
        Path to quarantined file
    """
    quarantine_dir = os.getenv("QUARANTINE_DIR", "./quarantine")
    os.makedirs(quarantine_dir, exist_ok=True)

    # Use hash in filename to prevent overwriting
    safe_filename = f"{file_hash[:16]}_{filename}"
    quarantine_path = os.path.join(quarantine_dir, safe_filename)

    # Save file
    with open(quarantine_path, "wb") as f:
        f.write(content)

    return quarantine_path


def get_file_type(filename: str) -> str:
    """
    Determine file type from filename

    Args:
        filename: Name of the file

    Returns:
        File type: 'pdf', 'markdown', or 'txt'
    """
    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        return "pdf"
    elif filename_lower.endswith((".md", ".markdown")):
        return "markdown"
    elif filename_lower.endswith(".txt"):
        return "txt"
    else:
        raise ValueError(f"Unsupported file type: {filename}")
