"""
Markdown Resume Parser Service
Parses markdown-formatted resumes into structured data for professional display.
Moved from frontend to prevent browser overload with large CVs.
"""

import re
from typing import Any, Dict, List, Optional


class ResumeData:
    """Structured resume data model"""

    def __init__(self):
        self.personal_info = {
            "name": "",
            "title": "",
            "summary": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "website": "",
        }
        self.experience: List[Dict] = []
        self.skills = {"languages": "", "tools": ""}
        self.education = {"school": "", "degree": "", "period": ""}
        self.certifications: List[str] = []

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "personalInfo": self.personal_info,
            "experience": self.experience,
            "skills": self.skills,
            "education": self.education,
            "certifications": self.certifications,
        }


class MarkdownResumeParser:
    """Parser for markdown-formatted resumes"""

    @staticmethod
    def convert_markdown_to_html(text: str) -> str:
        """Convert markdown formatting to HTML"""
        # Convert **text** to <strong>text</strong> (do this first)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # Convert *text* to <em>text</em> (single asterisks to italic)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        return text

    @staticmethod
    def extract_date_from_title(title: str) -> tuple:
        """
        Extract date from subsection title if present
        Returns (title_without_date, date)
        """
        # Common date patterns at the end: "Title | Date" or "Title - Date"
        date_pattern = r"^(.+?)\s*[\|–—-]\s*(.+?)$"
        match = re.search(date_pattern, title)
        if match:
            return (match.group(1).strip(), match.group(2).strip())
        return (title, None)

    @staticmethod
    def parse_sections(markdown: str) -> Dict[str, Any]:
        """
        Parse markdown into hierarchical sections and subsections

        Args:
            markdown: Markdown-formatted text

        Returns:
            Dictionary with sections and subsections structure
        """
        sections = []

        # Split by ## headers (main sections)
        section_pattern = re.compile(r"^##\s+(.+?)$", re.MULTILINE)
        subsection_pattern = re.compile(r"^###\s+(.+?)$", re.MULTILINE)

        # Find all main sections
        section_matches = list(section_pattern.finditer(markdown))

        for i, section_match in enumerate(section_matches):
            section_title = section_match.group(1).strip()
            section_start = section_match.end()

            # Skip "Contact Information" section as we display it separately in the header
            if re.match(r"contact\s+information", section_title, re.IGNORECASE):
                continue

            # Find the end of this section (start of next section or end of document)
            section_end = (
                section_matches[i + 1].start()
                if i + 1 < len(section_matches)
                else len(markdown)
            )
            section_content = markdown[section_start:section_end].strip()

            # Parse subsections within this section
            subsections = []
            subsection_matches = list(subsection_pattern.finditer(section_content))

            if subsection_matches:
                # Section has subsections
                for j, subsection_match in enumerate(subsection_matches):
                    subsection_title_raw = subsection_match.group(1).strip()
                    subsection_start = subsection_match.end()

                    # Extract date from title if present
                    subsection_title, subsection_date = (
                        MarkdownResumeParser.extract_date_from_title(
                            subsection_title_raw
                        )
                    )

                    # Find the end of this subsection
                    subsection_end = (
                        subsection_matches[j + 1].start()
                        if j + 1 < len(subsection_matches)
                        else len(section_content)
                    )
                    subsection_content = section_content[
                        subsection_start:subsection_end
                    ].strip()

                    # Parse bullet points and regular content
                    bullets_raw = re.findall(
                        r"^\s*[-•*]\s+(.+)$", subsection_content, re.MULTILINE
                    )
                    # Convert markdown to HTML in bullets
                    bullets = [
                        MarkdownResumeParser.convert_markdown_to_html(b)
                        for b in bullets_raw
                    ]

                    # Get non-bullet content (paragraphs)
                    paragraphs = []
                    lines = subsection_content.split("\n")
                    current_paragraph = []

                    for line in lines:
                        line = line.strip()
                        if line and not re.match(r"^\s*[-•*]\s+", line):
                            current_paragraph.append(line)
                        elif current_paragraph:
                            para_text = " ".join(current_paragraph)
                            # Convert markdown to HTML
                            paragraphs.append(
                                MarkdownResumeParser.convert_markdown_to_html(para_text)
                            )
                            current_paragraph = []

                    if current_paragraph:
                        para_text = " ".join(current_paragraph)
                        paragraphs.append(
                            MarkdownResumeParser.convert_markdown_to_html(para_text)
                        )

                    subsections.append(
                        {
                            "title": subsection_title,
                            "date": subsection_date,
                            "content": subsection_content,
                            "paragraphs": paragraphs,
                            "bullets": bullets,
                        }
                    )
            else:
                # Section has no subsections, treat content as single block
                bullets_raw = re.findall(
                    r"^\s*[-•*]\s+(.+)$", section_content, re.MULTILINE
                )
                # Convert markdown to HTML in bullets
                bullets = [
                    MarkdownResumeParser.convert_markdown_to_html(b)
                    for b in bullets_raw
                ]

                # Get paragraphs
                paragraphs = []
                lines = section_content.split("\n")
                current_paragraph = []

                for line in lines:
                    line = line.strip()
                    if line and not re.match(r"^\s*[-•*]\s+", line):
                        current_paragraph.append(line)
                    elif current_paragraph:
                        para_text = " ".join(current_paragraph)
                        # Convert markdown to HTML
                        paragraphs.append(
                            MarkdownResumeParser.convert_markdown_to_html(para_text)
                        )
                        current_paragraph = []

                if current_paragraph:
                    para_text = " ".join(current_paragraph)
                    paragraphs.append(
                        MarkdownResumeParser.convert_markdown_to_html(para_text)
                    )

            sections.append(
                {
                    "title": section_title,
                    "content": section_content,
                    "subsections": subsections,
                    "paragraphs": paragraphs if not subsections else [],
                    "bullets": re.findall(
                        r"^\s*[-•*]\s+(.+)$", section_content, re.MULTILINE
                    )
                    if not subsections
                    else [],
                }
            )

        return {"sections": sections, "total_sections": len(sections)}

    @staticmethod
    def parse_markdown(markdown: str) -> dict:
        """
        Parse markdown resume into structured data

        Args:
            markdown: Markdown-formatted resume text

        Returns:
            Dictionary containing structured resume data
        """
        data = ResumeData()

        # Extract name (first line or first # heading)
        name_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE) or re.search(
            r"^([A-Z][a-z]+\s+[A-Z][a-z]+)", markdown, re.MULTILINE
        )
        if name_match:
            data.personal_info["name"] = name_match.group(1).strip()

        # Extract email
        email_match = re.search(
            r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", markdown
        )
        if email_match:
            data.personal_info["email"] = email_match.group(1)

        # Extract phone
        phone_match = re.search(r"Phone:\s*([\+\d\s\(\)-]+)|(\+?\d{10,})", markdown)
        if phone_match:
            data.personal_info["phone"] = (
                phone_match.group(1) or phone_match.group(2)
            ).strip()

        # Extract LinkedIn
        linkedin_match = re.search(r"linkedin\.com\/[^\s,\)]+", markdown, re.IGNORECASE)
        if linkedin_match:
            data.personal_info["linkedin"] = linkedin_match.group(0)

        # Extract GitHub or website
        github_match = re.search(r"github\.com\/[^\s,\)]+", markdown, re.IGNORECASE)
        if github_match:
            data.personal_info["website"] = github_match.group(0)

        # Extract location
        location_match = re.search(
            r"Location:\s*([^\n]+)|Cairo,\s*Egypt", markdown, re.IGNORECASE
        )
        if location_match:
            data.personal_info["location"] = location_match.group(
                1
            ) or location_match.group(0)

        # Extract Professional Summary
        summary_match = re.search(
            r"##\s*Professional\s+Summary\s*\n+([\s\S]+?)(?=\n##|\n###|$)",
            markdown,
            re.IGNORECASE,
        )
        if summary_match:
            data.personal_info["summary"] = (
                summary_match.group(1).strip().replace("**", "")
            )
        else:
            # Try to extract from beginning if no section header
            lines = markdown.split("\n")
            summary_text = ""
            found_contact = False
            for i, line in enumerate(lines[:15]):
                line = line.strip()
                if any(
                    keyword in line
                    for keyword in ["Full Stack", "Engineer", "Developer"]
                ):
                    data.personal_info["title"] = re.sub(r"[*#]", "", line).strip()
                if (
                    len(line) > 50
                    and not line.startswith("#")
                    and "@" not in line
                    and not found_contact
                ):
                    summary_text += line + " "
                if "@" in line:
                    found_contact = True

            if summary_text and not data.personal_info["summary"]:
                data.personal_info["summary"] = summary_text.strip()[:500]

        # Extract title if not found
        if not data.personal_info["title"]:
            title_match = re.search(
                r"(?:Full Stack|Software|Backend|Frontend|Senior|Junior)\s+(?:Engineer|Developer)",
                markdown,
                re.IGNORECASE,
            )
            if title_match:
                data.personal_info["title"] = title_match.group(0)

        # Extract Skills
        data.skills = MarkdownResumeParser._extract_skills(markdown)

        # Extract Experience
        data.experience = MarkdownResumeParser._extract_experience(markdown)

        # Extract Education
        data.education = MarkdownResumeParser._extract_education(markdown)

        # Extract Certifications
        data.certifications = MarkdownResumeParser._extract_certifications(markdown)

        return data.to_dict()

    @staticmethod
    def _extract_skills(markdown: str) -> dict:
        """Extract skills section from markdown"""
        skills = {"languages": "", "tools": ""}

        skills_match = re.search(
            r"##\s*(?:Technical\s+)?Skills\s*\n+([\s\S]+?)(?=\n##|$)",
            markdown,
            re.IGNORECASE,
        )

        if not skills_match:
            return skills

        skills_text = skills_match.group(1)

        # Try to parse bulleted list format
        frontend_match = re.search(
            r"^\s*[-•*]\s*(?:Frontend|Front-?End):\s*(.+?)$",
            skills_text,
            re.IGNORECASE | re.MULTILINE,
        )
        backend_match = re.search(
            r"^\s*[-•*]\s*(?:Backend|Back-?End):\s*(.+?)$",
            skills_text,
            re.IGNORECASE | re.MULTILINE,
        )
        cloud_match = re.search(
            r"^\s*[-•*]\s*(?:Cloud\s*(?:&|and)?\s*DevOps):\s*(.+?)$",
            skills_text,
            re.IGNORECASE | re.MULTILINE,
        )
        testing_match = re.search(
            r"^\s*[-•*]\s*(?:Testing\s*(?:&|and)?\s*Quality):\s*(.+?)$",
            skills_text,
            re.IGNORECASE | re.MULTILINE,
        )
        other_match = re.search(
            r"^\s*[-•*]\s*(?:Other):\s*(.+?)$",
            skills_text,
            re.IGNORECASE | re.MULTILINE,
        )

        # Try markdown bold format
        front_end_match = re.search(
            r"\*\*Front-?End\*\*:?\s*(.+?)(?=\n\*\*|\n##|$)",
            skills_text,
            re.IGNORECASE | re.DOTALL,
        )
        back_end_match = re.search(
            r"\*\*Back-?End\*\*:?\s*(.+?)(?=\n\*\*|\n##|$)",
            skills_text,
            re.IGNORECASE | re.DOTALL,
        )
        tools_match = re.search(
            r"\*\*(?:Tools?\s*(?:&|and)?\s*(?:Platforms?|DevOps)|Cloud\s*(?:&|and)?\s*DevOps)\*\*:?\s*(.+?)(?=\n\*\*|\n##|$)",
            skills_text,
            re.IGNORECASE | re.DOTALL,
        )

        langs = []
        tools = []

        if frontend_match:
            langs.append(frontend_match.group(1).strip())
        if backend_match:
            langs.append(backend_match.group(1).strip())
        if front_end_match:
            langs.append(front_end_match.group(1).strip())
        if back_end_match:
            langs.append(back_end_match.group(1).strip())

        if cloud_match:
            tools.append(cloud_match.group(1).strip())
        if testing_match:
            tools.append(testing_match.group(1).strip())
        if other_match:
            tools.append(other_match.group(1).strip())
        if tools_match:
            tools.append(tools_match.group(1).strip())

        if langs:
            skills["languages"] = (
                ", ".join(langs).replace("\n", " ").replace("  ", " ").replace("**", "")
            )

        if tools:
            skills["tools"] = (
                ", ".join(tools).replace("\n", " ").replace("  ", " ").replace("**", "")
            )

        # Fallback: just grab all skills text
        if not skills["languages"] and not skills["tools"]:
            all_skills = skills_text.replace("**", "").replace("\n", ", ").strip()
            skills["languages"] = all_skills[:200]
            skills["tools"] = all_skills[200:400]

        return skills

    @staticmethod
    def _extract_experience(markdown: str) -> List[Dict]:
        """Extract experience section from markdown"""
        experience_match = re.search(
            r"##\s*(?:Professional\s+)?(?:Work\s+)?Experience\s*\n+([\s\S]+?)(?=\n##|$)",
            markdown,
            re.IGNORECASE,
        )

        if not experience_match:
            return []

        exp_section = experience_match.group(1)
        jobs = []

        # Split by job entries - look for role/title patterns followed by em dash or pipe
        job_pattern = re.compile(r"^(.+?)\s+[–—-]\s+(.+?)\s*\|\s*(.+?)$", re.MULTILINE)
        matches = list(job_pattern.finditer(exp_section))

        for i, match in enumerate(matches):
            role = match.group(1).strip()
            company = match.group(2).strip()
            period = match.group(3).strip()
            start_pos = match.end()

            # Get the content until the next job or end
            end_pos = (
                matches[i + 1].start() if i + 1 < len(matches) else len(exp_section)
            )
            job_content = exp_section[start_pos:end_pos]

            # Extract bullet points
            bullets = re.findall(r"^\s{4,}[-•*]\s*(.+)$", job_content, re.MULTILINE)
            description = [b.strip() for b in bullets]

            jobs.append(
                {
                    "role": role,
                    "company": company,
                    "period": period,
                    "description": description,
                }
            )

        # Fallback to original parsing if new method doesn't work
        if not jobs:
            exp_entries = re.split(r"(?=###)", exp_section)
            for entry in exp_entries:
                entry = entry.strip()
                if not entry:
                    continue

                job_match = re.search(r"###\s*(.+?)(?:\n|$)", entry)
                period_match = re.search(r"\*(.+?)\*", entry)

                if job_match:
                    job_line = job_match.group(1)
                    parts = re.split(r"\s*\|\s*", job_line)

                    experience = {
                        "role": parts[0].strip() if parts else "",
                        "company": parts[1].strip()
                        if len(parts) > 1
                        else "Confidential",
                        "period": period_match.group(1).strip() if period_match else "",
                        "description": [],
                    }

                    # Extract bullet points
                    bullets = re.findall(r"^\s*[-•]\s*(.+)$", entry, re.MULTILINE)
                    if bullets:
                        experience["description"] = [b.strip() for b in bullets]

                    jobs.append(experience)

        return jobs

    @staticmethod
    def _extract_education(markdown: str) -> dict:
        """Extract education section from markdown"""
        education = {"school": "", "degree": "", "period": ""}

        education_match = re.search(
            r"##\s*Education\s*\n+([\s\S]+?)(?=\n##|$)", markdown, re.IGNORECASE
        )

        if not education_match:
            return education

        edu_section = education_match.group(1)

        # Try new format: "Degree – School | Period"
        edu_pattern = re.search(
            r"^(.+?)\s+[–—-]\s+(.+?)\s*\|\s*(.+?)$", edu_section, re.MULTILINE
        )

        if edu_pattern:
            education["degree"] = edu_pattern.group(1).strip()
            education["school"] = edu_pattern.group(2).strip()
            education["period"] = edu_pattern.group(3).strip()
        else:
            # Fallback to old format
            degree_match = re.search(r"###\s*(.+?)(?:\n|$)", edu_section)
            period_match = re.search(r"\*(.+?)\*", edu_section)

            if degree_match:
                parts = re.split(r"\s*\|\s*", degree_match.group(1))
                education["degree"] = parts[0].strip() if parts else ""
                education["school"] = parts[1].strip() if len(parts) > 1 else ""
                education["period"] = (
                    period_match.group(1).strip() if period_match else ""
                )

        return education

    @staticmethod
    def _extract_certifications(markdown: str) -> List[str]:
        """Extract certifications section from markdown"""
        certs_match = re.search(
            r"##\s*Certifications?\s*\n+([\s\S]+?)(?=\n##|$)", markdown, re.IGNORECASE
        )

        if not certs_match:
            return []

        bullets = re.findall(r"^\s*[-•]\s*(.+)$", certs_match.group(1), re.MULTILINE)
        return [b.strip() for b in bullets]


# Singleton instance
markdown_parser = MarkdownResumeParser()
