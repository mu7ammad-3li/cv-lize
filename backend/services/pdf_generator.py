"""
PDF Generation Service using WeasyPrint
Generates professional PDFs from optimized CV data
"""

import os
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration

# Get the templates directory
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class PDFGenerator:
    """Service for generating PDF documents from templates"""

    def __init__(self):
        """Initialize Jinja2 environment and WeasyPrint font configuration"""
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.font_config = FontConfiguration()

    def generate_cv_pdf(
        self,
        personal_info: dict,
        sections: Optional[dict] = None,
        experience: Optional[list] = None,
        skills: Optional[dict] = None,
        education: Optional[dict] = None,
        certifications: Optional[list] = None,
    ) -> bytes:
        """
        Generate a professional CV PDF from structured data

        Args:
            personal_info: Personal information (name, title, email, phone, etc.)
            sections: Structured sections from markdown parser (preferred)
            experience: Work experience data (fallback)
            skills: Technical skills (fallback)
            education: Education data (fallback)
            certifications: Certifications list (fallback)

        Returns:
            PDF file content as bytes
        """
        # Load template - Using v2 with ATS-friendly formatting
        template = self.env.get_template("professional_structured_v2.html")

        # Render HTML with data
        html_content = template.render(
            personal_info=personal_info,
            sections=sections,
            experience=experience,
            skills=skills,
            education=education,
            certifications=certifications,
        )

        # Generate PDF using WeasyPrint
        html_doc = HTML(string=html_content)
        pdf_bytes = html_doc.write_pdf(font_config=self.font_config)

        return pdf_bytes

    def generate_from_parsed_resume(
        self, parsed_resume: dict, sections: Optional[dict] = None
    ) -> bytes:
        """
        Generate PDF from ParsedResumeData

        Args:
            parsed_resume: ParsedResumeData dictionary
            sections: Optional CVSections structure

        Returns:
            PDF file content as bytes
        """
        return self.generate_cv_pdf(
            personal_info=parsed_resume.get("personalInfo", {}),
            sections=sections,
            experience=parsed_resume.get("experience", []),
            skills=parsed_resume.get("skills", {}),
            education=parsed_resume.get("education", {}),
            certifications=parsed_resume.get("certifications", []),
        )


# Singleton instance
pdf_generator = PDFGenerator()
