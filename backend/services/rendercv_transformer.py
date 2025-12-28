"""
RenderCV Data Transformer Service
Converts CV-lize parsed data into RenderCV YAML format
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from models.schemas import CVSection, CVSections


class RenderCVTransformer:
    """Transform CV-lize data structures to RenderCV YAML format"""

    # ATS-safe fonts supported by RenderCV
    SUPPORTED_FONTS = [
        "Arial",
        "Calibri",
        "Helvetica",
        "Times New Roman",
        "Georgia",
        "Garamond",
        "Raleway",
        "Open Sans",
        "Lato",
        "Source Sans 3",
    ]

    @staticmethod
    def parse_date_range(date_str: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse date range string into start_date and end_date

        Examples:
            "Jan 2020 - Present" -> ("2020-01", "present")
            "2018 - 2022" -> ("2018", "2022")
            "March 2021 - Dec 2023" -> ("2021-03", "2023-12")

        Args:
            date_str: Date range string

        Returns:
            Tuple of (start_date, end_date) in RenderCV format
        """
        if not date_str:
            return (None, None)

        # Handle "present", "current", "now"
        date_str = re.sub(
            r"\b(present|current|now)\b", "present", date_str, flags=re.IGNORECASE
        )

        # Split by common separators
        parts = re.split(r"\s*[-–—to|]\s*", date_str, maxsplit=1)

        def parse_single_date(date_part: str) -> Optional[str]:
            """Parse a single date component"""
            date_part = date_part.strip()

            if not date_part or date_part.lower() == "present":
                return "present" if date_part.lower() == "present" else None

            # Month mapping
            month_map = {
                "jan": "01",
                "january": "01",
                "feb": "02",
                "february": "02",
                "mar": "03",
                "march": "03",
                "apr": "04",
                "april": "04",
                "may": "05",
                "jun": "06",
                "june": "06",
                "jul": "07",
                "july": "07",
                "aug": "08",
                "august": "08",
                "sep": "09",
                "sept": "09",
                "september": "09",
                "oct": "10",
                "october": "10",
                "nov": "11",
                "november": "11",
                "dec": "12",
                "december": "12",
            }

            # Try to match "Month Year" or "Month YYYY"
            month_year = re.search(
                r"([a-z]+)\s+(\d{4})", date_part, flags=re.IGNORECASE
            )
            if month_year:
                month_name = month_year.group(1).lower()
                year = month_year.group(2)
                if month_name in month_map:
                    return f"{year}-{month_map[month_name]}"

            # Try to match just year "YYYY"
            year_match = re.search(r"\b(\d{4})\b", date_part)
            if year_match:
                return year_match.group(1)

            return None

        start_date = parse_single_date(parts[0]) if len(parts) > 0 else None
        end_date = parse_single_date(parts[1]) if len(parts) > 1 else None

        return (start_date, end_date)

    @staticmethod
    def clean_markdown(text: str) -> str:
        """
        Convert HTML tags back to Markdown for RenderCV

        Args:
            text: Text with HTML tags

        Returns:
            Text with Markdown syntax
        """
        # Convert HTML to Markdown
        text = re.sub(r"<strong>(.*?)</strong>", r"**\1**", text)
        text = re.sub(r"<b>(.*?)</b>", r"**\1**", text)
        text = re.sub(r"<em>(.*?)</em>", r"*\1*", text)
        text = re.sub(r"<i>(.*?)</i>", r"*\1*", text)
        return text

    @staticmethod
    def ensure_url_scheme(url: str) -> str:
        """
        Ensure URL has a scheme (https://)

        Args:
            url: URL string that may or may not have a scheme

        Returns:
            URL with https:// scheme
        """
        if not url:
            return ""

        # If already has scheme, return as is
        if url.startswith(("http://", "https://")):
            return url

        # Add https:// prefix
        return f"https://{url}"

    def transform_personal_info(self, personal_info: dict) -> dict:
        """
        Transform personal information to RenderCV cv field

        Args:
            personal_info: Personal info dictionary

        Returns:
            RenderCV cv field dictionary
        """
        # Ensure website has proper URL scheme
        website = personal_info.get("website", "")
        if website:
            website = self.ensure_url_scheme(website)

        cv_data = {
            "name": personal_info.get("name", ""),
            "location": personal_info.get("location", ""),
            "email": personal_info.get("email", ""),
            "phone": personal_info.get("phone", ""),
            "website": website,
        }

        # Handle social networks
        social_networks = []
        if linkedin := personal_info.get("linkedin"):
            # Extract username from URL if present
            linkedin_match = re.search(r"linkedin\.com/in/([^/\s]+)", linkedin)
            username = linkedin_match.group(1) if linkedin_match else linkedin
            social_networks.append({"network": "LinkedIn", "username": username})

        if github := personal_info.get("github"):
            github_match = re.search(r"github\.com/([^/\s]+)", github)
            username = github_match.group(1) if github_match else github
            social_networks.append({"network": "GitHub", "username": username})

        if social_networks:
            cv_data["social_networks"] = social_networks

        return cv_data

    def transform_summary(self, personal_info: dict) -> Optional[List[str]]:
        """
        Transform Professional Summary to TextEntry

        Args:
            personal_info: Personal info with summary field

        Returns:
            List containing summary text (TextEntry format)
        """
        if summary := personal_info.get("summary"):
            # Clean and format summary
            summary = self.clean_markdown(summary)
            return [summary.strip()]
        return None

    def transform_experience(self, experience: list) -> List[dict]:
        """
        Transform experience to RenderCV ExperienceEntry format

        Args:
            experience: List of experience dictionaries

        Returns:
            List of RenderCV ExperienceEntry dictionaries
        """
        entries = []

        for exp in experience:
            entry = {
                "company": exp.get("company", ""),
                "position": exp.get("role", exp.get("position", "")),
            }

            # Add location if present
            if location := exp.get("location"):
                entry["location"] = location

            # Parse dates
            if period := exp.get("period"):
                start_date, end_date = self.parse_date_range(period)
                if start_date:
                    entry["start_date"] = start_date
                if end_date:
                    entry["end_date"] = end_date

            # Add highlights (bullet points)
            if description := exp.get("description"):
                if isinstance(description, list):
                    entry["highlights"] = [
                        self.clean_markdown(item) for item in description
                    ]
                elif isinstance(description, str):
                    entry["highlights"] = [self.clean_markdown(description)]

            entries.append(entry)

        return entries

    def transform_education(self, education: dict) -> List[dict]:
        """
        Transform education to RenderCV EducationEntry format

        Args:
            education: Education dictionary

        Returns:
            List of RenderCV EducationEntry dictionaries
        """
        if not education or not education.get("degree"):
            return []

        entry = {
            "institution": education.get("school", ""),
            "degree": education.get("degree", ""),
        }

        # Extract area/field from degree if possible
        degree_str = education.get("degree", "")
        # Try to extract field like "Bachelor of Science in Computer Science"
        field_match = re.search(
            r"(?:in|of)\s+([A-Z][^,\n]+)", degree_str, flags=re.IGNORECASE
        )
        if field_match:
            entry["area"] = field_match.group(1).strip()
            # Simplify degree to just "Bachelor", "Master", etc.
            entry["degree"] = re.sub(
                r"\s+(?:in|of)\s+.*", "", degree_str, flags=re.IGNORECASE
            ).strip()

        # Parse dates
        if period := education.get("period"):
            start_date, end_date = self.parse_date_range(period)
            if start_date:
                entry["start_date"] = start_date
            if end_date:
                entry["end_date"] = end_date

        # Add location if present
        if location := education.get("location"):
            entry["location"] = location

        # Add GPA and honors as highlights
        highlights = []
        if gpa := education.get("gpa"):
            highlights.append(f"GPA: {gpa}")
        if honors := education.get("honors"):
            highlights.append(honors)

        if highlights:
            entry["highlights"] = highlights

        return [entry]

    def transform_skills(self, skills: dict) -> List[dict]:
        """
        Transform skills to RenderCV OneLineEntry format

        Args:
            skills: Skills dictionary

        Returns:
            List of RenderCV OneLineEntry dictionaries
        """
        entries = []

        for category, items in skills.items():
            if not items:
                continue

            # Format category name
            label = category.replace("_", " ").title()

            # Handle both string and list formats
            if isinstance(items, list):
                details = ", ".join(str(item) for item in items)
            else:
                details = str(items)

            entries.append({"label": label, "details": details})

        return entries

    def transform_certifications(self, certifications: list) -> List[dict]:
        """
        Transform certifications to RenderCV BulletEntry format

        Args:
            certifications: List of certification strings

        Returns:
            List of RenderCV BulletEntry dictionaries
        """
        return [{"bullet": self.clean_markdown(cert)} for cert in certifications]

    def transform_custom_section(self, section: CVSection) -> Tuple[str, List[dict]]:
        """
        Transform custom CV section to appropriate RenderCV entry type

        Args:
            section: CVSection object

        Returns:
            Tuple of (entry_type, entries_list)
        """
        # If section has subsections, use NormalEntry
        if section.subsections and len(section.subsections) > 0:
            entries = []
            for sub in section.subsections:
                # Get title and handle attributes
                title = (
                    getattr(sub, "title", "")
                    if hasattr(sub, "title")
                    else str(sub.get("title", ""))
                    if isinstance(sub, dict)
                    else ""
                )

                if not title:
                    continue

                entry = {"name": title}

                # Add date if present
                date = (
                    getattr(sub, "date", None)
                    if hasattr(sub, "date")
                    else sub.get("date")
                    if isinstance(sub, dict)
                    else None
                )
                if date:
                    entry["date"] = date

                # Add summary from paragraphs
                paragraphs = (
                    getattr(sub, "paragraphs", [])
                    if hasattr(sub, "paragraphs")
                    else sub.get("paragraphs", [])
                    if isinstance(sub, dict)
                    else []
                )
                if paragraphs:
                    summary = " ".join(paragraphs)
                    entry["summary"] = self.clean_markdown(summary)

                # Add highlights from bullets
                bullets = (
                    getattr(sub, "bullets", [])
                    if hasattr(sub, "bullets")
                    else sub.get("bullets", [])
                    if isinstance(sub, dict)
                    else []
                )
                if bullets:
                    entry["highlights"] = [
                        self.clean_markdown(bullet) for bullet in bullets
                    ]

                entries.append(entry)

            if entries:  # Only return if we have valid entries
                return ("NormalEntry", entries)

        # Section has no subsections
        # If has bullets only, use BulletEntry
        elif section.bullets:
            entries = [
                {"bullet": self.clean_markdown(bullet)} for bullet in section.bullets
            ]
            return ("BulletEntry", entries)

        # If has paragraphs only, use TextEntry
        elif section.paragraphs:
            entries = [self.clean_markdown(para) for para in section.paragraphs]
            return ("TextEntry", entries)

        # Fallback to TextEntry with content
        return ("TextEntry", [section.content])

    def transform_to_rendercv(
        self,
        personal_info: dict,
        sections: Optional[CVSections] = None,
        experience: Optional[list] = None,
        skills: Optional[dict] = None,
        education: Optional[dict] = None,
        certifications: Optional[list] = None,
        font_family: str = "Arial",
        theme: str = "engineeringresumes",
    ) -> dict:
        """
        Transform complete CV data to RenderCV YAML structure

        Args:
            personal_info: Personal information
            sections: Structured sections (preferred)
            experience: Fallback experience data
            skills: Fallback skills data
            education: Fallback education data
            certifications: Fallback certifications data
            font_family: Font to use (must be ATS-safe)
            theme: RenderCV theme (engineeringresumes, engineeringclassic, classic, etc.)

        Returns:
            Complete RenderCV YAML structure as dictionary
        """
        # Validate font
        if font_family not in self.SUPPORTED_FONTS:
            print(
                f"⚠️  Warning: {font_family} may not be ATS-safe. Using Arial instead."
            )
            font_family = "Arial"

        # Build CV data
        cv_data = self.transform_personal_info(personal_info)
        cv_sections = {}

        # Add Professional Summary if present
        if summary := self.transform_summary(personal_info):
            cv_sections["Professional Summary"] = summary

        # Process structured sections if available
        # Handle both CVSections object and dict format
        sections_list = None
        if sections:
            if isinstance(sections, dict):
                sections_list = sections.get("sections", [])
            elif hasattr(sections, "sections"):
                sections_list = sections.sections

        if sections_list:
            for section in sections_list:
                # Handle both dict and object format
                if isinstance(section, dict):
                    # Convert dict to CVSection-like object
                    from types import SimpleNamespace

                    section_obj = SimpleNamespace(**section)
                    # Convert subsections if present
                    if "subsections" in section and section["subsections"]:
                        section_obj.subsections = [
                            SimpleNamespace(**s) if isinstance(s, dict) else s
                            for s in section["subsections"]
                        ]
                    section = section_obj

                # Skip contact info and summary (already handled)
                title_lower = section.title.lower()
                if any(
                    skip in title_lower for skip in ["contact", "professional summary"]
                ):
                    continue

                # Determine entry type and transform
                entry_type, entries = self.transform_custom_section(section)

                # Add to sections
                if entries:
                    cv_sections[section.title] = entries

        # Fallback to traditional sections if no structured sections
        else:
            if experience:
                cv_sections["Experience"] = self.transform_experience(experience)

            if skills:
                cv_sections["Technical Skills"] = self.transform_skills(skills)

            if education:
                cv_sections["Education"] = self.transform_education(education)

            if certifications:
                cv_sections["Certifications"] = self.transform_certifications(
                    certifications
                )

        cv_data["sections"] = cv_sections

        # Build complete RenderCV structure
        rendercv_data = {
            "cv": cv_data,
            "design": self._get_design_config(font_family, theme),
            "locale": {"language": "english"},
            "settings": {
                "current_date": datetime.now().strftime("%Y-%m-%d"),
            },
        }

        return rendercv_data

    def _get_design_config(self, font_family: str, theme: str) -> dict:
        """
        Get RenderCV design configuration with ATS-safe settings

        Args:
            font_family: Font to use
            theme: RenderCV theme name

        Returns:
            Design configuration dictionary
        """
        return {
            "theme": theme,
            "typography": {
                "font_family": {
                    "body": font_family,
                    "name": font_family,
                    "headline": font_family,
                    "connections": font_family,
                    "section_titles": font_family,
                },
                "font_size": {
                    "body": "11pt",  # ATS: 10-12pt
                    "name": "28pt",  # ATS: 24-36pt
                    "headline": "11pt",
                    "connections": "10pt",
                    "section_titles": "14pt",  # ATS: 14-16pt
                },
                "line_spacing": "0.6em",
                "alignment": "justified",
                "bold": {
                    "name": True,
                    "section_titles": True,
                    "headline": False,
                    "connections": False,
                },
            },
            "page": {
                "size": "us-letter",
                "top_margin": "1in",
                "bottom_margin": "1in",
                "left_margin": "1in",
                "right_margin": "1in",
            },
        }


# Singleton instance
rendercv_transformer = RenderCVTransformer()
