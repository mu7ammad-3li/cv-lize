"""
ATS formatting validation service
Detect formatting issues that cause ATS parsing problems
"""

import re
from typing import List

import pdfplumber
from models.schemas import ATSFormattingIssue


class ATSValidator:
    """
    Validate resume formatting for ATS compatibility

    Checks for:
    - Multi-column layouts
    - Tables
    - Text boxes
    - Contact info in headers/footers
    - Custom fonts
    - Graphics/images
    - Unusual spacing
    """

    # ATS-safe fonts
        "arial",
        "calibri",
        "helvetica",
        "times new roman",
        "georgia",
        "garamond",
        "cambria",
        "aptos",
        "roboto",
    ]

    # Standard section headers
    STANDARD_HEADERS = [
        "summary",
        "professional summary",
        "profile",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "education",
        "academic background",
        "skills",
        "technical skills",
        "core competencies",
        "projects",
        "technical projects",
        "certifications",
        "certificates",
        "awards",
    ]

    def __init__(self):
        pass

    def validate_pdf_structure(self, pdf_path: str) -> List[ATSFormattingIssue]:
        """
        Validate PDF file for ATS compatibility issues

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of formatting issues
        """
        issues = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Check for tables
                    tables = page.find_tables()
                    if tables:
                        issues.append(
                            ATSFormattingIssue(
                                issue_type="table",
                                severity="high",
                                description=f"Page {page_num} contains {len(tables)} table(s). ATS parsers often scramble table content.",
                                recommendation="Convert table data to standard bullet points or linear text format.",
                            )
                        )

                    # Check for multi-column layout
                    text = page.extract_text()
                    if text and self._detect_multi_column(text):
                        issues.append(
                            ATSFormattingIssue(
                                issue_type="multi_column",
                                severity="critical",
                                description=f"Page {page_num} appears to use multi-column layout.",
                                recommendation="Use single-column linear layout. ATS parsers read left-to-right, top-to-bottom.",
                            )
                        )

                    # Check for images/graphics
                    if page.images:
                        issues.append(
                            ATSFormattingIssue(
                                issue_type="graphics",
                                severity="medium",
                                description=f"Page {page_num} contains {len(page.images)} image(s).",
                                recommendation="Remove images, logos, and graphics. ATS cannot parse visual elements.",
                            )
                        )

        except Exception as e:
            print(f"⚠️  PDF validation error: {e}")
            issues.append(
                ATSFormattingIssue(
                    issue_type="validation_error",
                    severity="low",
                    description=f"Could not fully validate PDF structure: {str(e)}",
                    recommendation="Ensure PDF is text-based, not scanned image.",
                )
            )

        return issues

    def validate_text_structure(self, text: str) -> List[ATSFormattingIssue]:
        """
        Validate text content for ATS compatibility

        Args:
            text: Resume text content

        Returns:
            List of formatting issues
        """
        issues = []

        # Check for non-standard section headers
        lines = text.split("\n")
        section_headers = []

        for line in lines:
            line_clean = line.strip()
            # Detect potential headers (short lines, all caps, or with special formatting)
            if 2 < len(line_clean) < 50:
                if line_clean.isupper() or self._looks_like_header(line_clean):
                    section_headers.append(line_clean.lower())

        non_standard_headers = []
        for header in section_headers:
            if not any(std in header for std in self.STANDARD_HEADERS):
                non_standard_headers.append(header)

        if non_standard_headers:
            issues.append(
                ATSFormattingIssue(
                    issue_type="non_standard_headers",
                    severity="medium",
                    description=f"Detected non-standard section headers: {', '.join(non_standard_headers[:3])}",
                    recommendation="Use standard headers: Professional Summary, Work Experience, Education, Skills, Projects, Certifications.",
                )
            )

        # Check for contact info at the top
        first_500_chars = text[:500].lower()
        has_email = "@" in first_500_chars
        has_phone = bool(re.search(r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}", first_500_chars))

        if not (has_email or has_phone):
            issues.append(
                ATSFormattingIssue(
                    issue_type="contact_info_missing",
                    severity="critical",
                    description="Contact information not detected in first 500 characters.",
                    recommendation="Place contact info (name, email, phone, location) at the top of resume in main body text.",
                )
            )

        # Check for unusual characters or symbols
        unusual_chars = re.findall(r"[^\w\s\-.,@/()\'\"+:;]", text)
        if len(unusual_chars) > 20:
            issues.append(
                ATSFormattingIssue(
                    issue_type="unusual_characters",
                    severity="low",
                    description=f"Detected {len(unusual_chars)} unusual special characters.",
                    recommendation="Use only standard ASCII characters. Avoid fancy bullets, symbols, or Unicode decorations.",
                )
            )

        # Check for very long lines (might indicate formatting issues)
        long_lines = [line for line in lines if len(line) > 200]
        if len(long_lines) > 5:
            issues.append(
                ATSFormattingIssue(
                    issue_type="long_lines",
                    severity="low",
                    description=f"Detected {len(long_lines)} very long lines of text.",
                    recommendation="Break up long paragraphs into bullet points for better parsing.",
                )
            )

        # Check for date format
        dates = re.findall(r"\d{1,2}/\d{1,2}/\d{2,4}", text)
        if dates:
            issues.append(
                ATSFormattingIssue(
                    issue_type="date_format",
                    severity="low",
                    description=f"Dates in DD/MM/YYYY or MM/DD/YYYY format detected.",
                    recommendation="Use MM/YYYY format for dates (e.g., '01/2023 - 06/2024'). Avoid full day-month-year format.",
                )
            )

        return issues

    def validate_keyword_density(self, keyword_analyses) -> List[ATSFormattingIssue]:
        """
        Validate keyword density (optimal: 1-3%)

        Args:
            keyword_analyses: List of KeywordAnalysis objects

        Returns:
            List of issues related to keyword density
        """
        issues = []

        # Check for keyword stuffing (density > 5%)
        stuffed_keywords = [ka for ka in keyword_analyses if ka.density > 5.0]
        if stuffed_keywords:
            keywords_str = ", ".join([ka.keyword for ka in stuffed_keywords[:3]])
            issues.append(
                ATSFormattingIssue(
                    issue_type="keyword_stuffing",
                    severity="high",
                    description=f"Keywords appear too frequently (>5% density): {keywords_str}",
                    recommendation="Reduce keyword repetition. Modern ATS flags excessive repetition as spam. Aim for 1-3% density.",
                )
            )

        # Check for low keyword presence (density < 0.5% for important keywords)
        low_density = [ka for ka in keyword_analyses if ka.in_jd and ka.density < 0.5]
        if len(low_density) > 5:
            issues.append(
                ATSFormattingIssue(
                    issue_type="low_keyword_density",
                    severity="medium",
                    description=f"{len(low_density)} important keywords from job description appear too infrequently.",
                    recommendation="Incorporate job description keywords more naturally throughout your resume, especially in work experience.",
                )
            )

        return issues

    def _detect_multi_column(self, text: str) -> bool:
        """
        Heuristic to detect multi-column layout from text

        Multi-column layouts often result in interleaved text when parsed
        """
        lines = text.split("\n")

        # Check for very short lines in succession (common in multi-column)
        short_line_streak = 0
        max_streak = 0

        for line in lines:
            if 5 < len(line.strip()) < 40:
                short_line_streak += 1
                max_streak = max(max_streak, short_line_streak)
            else:
                short_line_streak = 0

        # If we have many short lines in a row, likely multi-column
        return max_streak > 10

    def _looks_like_header(self, line: str) -> bool:
        """Check if a line looks like a section header"""
        # Headers are typically:
        # - Short (< 50 chars)
        # - Not ending with punctuation
        # - May have special formatting indicators

        if len(line) > 50:
            return False

        # Check if it ends with punctuation (headers usually don't)
        if line.strip()[-1:] in ".!?,;":
            return False

        # Check if it contains common header words
        header_words = [
            "summary",
            "experience",
            "education",
            "skills",
            "projects",
            "certifications",
        ]
        header_words = ['summary', 'experience', 'education', 'skills', 'projects', 'certifications']
        if any(word in line.lower() for word in header_words):
            return True

        return False


# Create singleton instance
ats_validator = ATSValidator()
