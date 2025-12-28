"""
PDF Generation Service using WeasyPrint
Generates professional PDFs from optimized CV data
"""

import os
from pathlib import Path
from typing import Optional

import weasyprint
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
        font_family: str = "Arial",
        pdf_variant: Optional[str] = None,
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
            font_family: Font family to use for the PDF
            pdf_variant: PDF standard variant (None, 'pdf/a-1b', 'pdf/a-2b', 'pdf/a-3b', 'pdf/a-3u', 'pdf/ua-1')
                        'pdf/a-3u' recommended for best ATS compatibility

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
            font_family=font_family,
        )

        # Generate PDF using WeasyPrint with optional PDF/A compliance
        html_doc = HTML(string=html_content)

        # Prepare PDF generation parameters
        pdf_params = {"font_config": self.font_config}

        # Add PDF variant if specified (for ATS compliance)
        # Note: PDF/A support is experimental in WeasyPrint and may not be available in all versions
        if pdf_variant:
            try:
                # Check if pdf_variant is supported
                import inspect

                sig = inspect.signature(html_doc.write_pdf)
                if "pdf_variant" in sig.parameters:
                    pdf_params["pdf_variant"] = pdf_variant
                    print(
                        f"📋 Generating PDF with variant: {pdf_variant} for enhanced ATS compatibility"
                    )
                else:
                    print(
                        f"⚠️  PDF/A variant not supported in WeasyPrint {weasyprint.__version__}, using standard PDF"
                    )
            except Exception as e:
                print(f"⚠️  Could not enable PDF/A variant: {e}")

        pdf_bytes = html_doc.write_pdf(**pdf_params)

        return pdf_bytes

    def generate_from_parsed_resume(
        self,
        parsed_resume: dict,
        sections: Optional[dict] = None,
        font_family: str = "Arial",
        pdf_variant: Optional[str] = "pdf/a-3u",
    ) -> bytes:
        """
        Generate PDF from ParsedResumeData

        Args:
            parsed_resume: ParsedResumeData dictionary
            sections: Optional CVSections structure
            font_family: Font family to use for the PDF
            pdf_variant: PDF standard variant for ATS compliance (default: 'pdf/a-3u')

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
            font_family=font_family,
            pdf_variant=pdf_variant,
        )


# Singleton instance
pdf_generator = PDFGenerator()
