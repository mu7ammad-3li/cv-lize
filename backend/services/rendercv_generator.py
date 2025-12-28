"""
RenderCV PDF Generation Service
Generates professional PDFs using RenderCV and Typst
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

import yaml

from services.rendercv_transformer import rendercv_transformer


class RenderCVGenerator:
    """Service for generating PDF documents using RenderCV"""

    def __init__(self):
        """Initialize RenderCV generator"""
        self.transformer = rendercv_transformer

    def generate_cv_pdf(
        self,
        personal_info: dict,
        sections: Optional[dict] = None,
        experience: Optional[list] = None,
        skills: Optional[dict] = None,
        education: Optional[dict] = None,
        certifications: Optional[list] = None,
        font_family: str = "Arial",
        theme: str = "engineeringresumes",
    ) -> bytes:
        """
        Generate a professional CV PDF using RenderCV

        Args:
            personal_info: Personal information (name, title, email, phone, etc.)
            sections: Structured sections from markdown parser (preferred)
            experience: Work experience data (fallback)
            skills: Technical skills (fallback)
            education: Education data (fallback)
            certifications: Certifications list (fallback)
            font_family: Font family to use (default: Arial)
            theme: RenderCV theme (default: engineeringresumes)

        Returns:
            PDF file content as bytes
        """
        try:
            # Import RenderCV - check if it's installed
            import rendercv
        except ImportError:
            raise ImportError(
                "RenderCV is not installed. Please run: pip install 'rendercv[full]==2.5'"
            )

        # Transform data to RenderCV format
        rendercv_data = self.transformer.transform_to_rendercv(
            personal_info=personal_info,
            sections=sections,
            experience=experience,
            skills=skills,
            education=education,
            certifications=certifications,
            font_family=font_family,
            theme=theme,
        )

        # Create temporary directory for RenderCV output
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Generate safe filename from name
            name = personal_info.get("name", "resume")
            safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "_"))
            safe_name = safe_name.replace(" ", "_")

            # Write YAML file
            yaml_file = temp_path / f"{safe_name}_CV.yaml"
            with open(yaml_file, "w", encoding="utf-8") as f:
                yaml.dump(
                    rendercv_data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            # Generate PDF using RenderCV
            try:
                # Run RenderCV via subprocess (most reliable method)
                import subprocess

                cmd = [
                    "rendercv",
                    "render",
                    str(yaml_file),
                    "--output-folder-name",
                    str(temp_path / "rendercv_output"),
                ]

                result = subprocess.run(
                    cmd, capture_output=True, text=True, cwd=str(temp_path), timeout=30
                )

                if result.returncode != 0:
                    error_msg = result.stderr or result.stdout
                    raise RuntimeError(f"RenderCV command failed: {error_msg}")

                # Find generated PDF
                pdf_file = temp_path / "rendercv_output" / f"{safe_name}_CV.pdf"

                if not pdf_file.exists():
                    # Try alternative path
                    pdf_file = temp_path / f"{safe_name}_CV.pdf"

                if not pdf_file.exists():
                    # Search for any PDF in output
                    pdf_files = list(temp_path.glob("**/*.pdf"))
                    if pdf_files:
                        pdf_file = pdf_files[0]
                    else:
                        raise FileNotFoundError(
                            f"PDF file not found after RenderCV generation. Searched: {temp_path}"
                        )

                # Read PDF bytes
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()

                return pdf_bytes

            except Exception as e:
                raise RuntimeError(f"RenderCV PDF generation failed: {str(e)}")

    def generate_from_parsed_resume(
        self,
        parsed_resume: dict,
        sections: Optional[dict] = None,
        font_family: str = "Arial",
        theme: str = "engineeringresumes",
    ) -> bytes:
        """
        Generate PDF from ParsedResumeData

        Args:
            parsed_resume: ParsedResumeData dictionary
            sections: Optional CVSections structure
            font_family: Font family to use for the PDF
            theme: RenderCV theme to use

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
            theme=theme,
        )

    def get_available_themes(self) -> list:
        """
        Get list of available RenderCV themes

        Returns:
            List of theme names
        """
        return [
            "engineeringresumes",
            "engineeringclassic",
            "classic",
            "sb2nov",
            "moderncv",
        ]

    def get_available_fonts(self) -> list:
        """
        Get list of ATS-safe fonts supported by RenderCV

        Returns:
            List of font names
        """
        return self.transformer.SUPPORTED_FONTS


# Singleton instance
rendercv_generator = RenderCVGenerator()
