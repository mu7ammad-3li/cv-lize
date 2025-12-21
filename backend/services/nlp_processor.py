"""
NLP Processor for CV entity extraction using spaCy
Direct integration - no subprocess overhead
"""

import re
from typing import Dict, List, Optional

import spacy

from models.schemas import ContactInfo, Education, Experience, ParsedCVData


class CVParser:
    """Parse CV text and extract structured entities using spaCy"""

    def __init__(self):
        """Load spaCy model once at initialization (shared across requests)"""
        try:
            # Try to load the medium model first
            self.nlp = spacy.load("en_core_web_md")
            print("✅ Loaded spaCy model: en_core_web_md")
        except OSError:
            try:
                # Fallback to small model if medium not available
                self.nlp = spacy.load("en_core_web_sm")
                print("⚠️  Using fallback spaCy model: en_core_web_sm")
            except OSError:
                print(
                    "❌ No spaCy model found. Please run: python -m spacy download en_core_web_md"
                )
                raise

        # Common technical skills (expandable)
        self.technical_skills = {
            "python",
            "java",
            "javascript",
            "typescript",
            "c++",
            "c#",
            "ruby",
            "php",
            "go",
            "rust",
            "swift",
            "kotlin",
            "react",
            "angular",
            "vue",
            "node.js",
            "django",
            "flask",
            "fastapi",
            "spring",
            "express",
            "mongodb",
            "postgresql",
            "mysql",
            "redis",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "git",
            "ci/cd",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "pandas",
            "numpy",
            "html",
            "css",
            "sass",
            "webpack",
            "bash",
            "linux",
            "windows",
        }

        # Email regex pattern
        self.email_pattern = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )

        # Phone regex pattern (various formats)
        self.phone_pattern = re.compile(
            r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|"
            r"\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
        )

        # LinkedIn URL pattern
        self.linkedin_pattern = re.compile(r"linkedin\.com/in/[\w-]+")

    async def extract_cv_entities(self, text: str) -> ParsedCVData:
        """
        Extract all entities from CV text

        Args:
            text: Raw CV text

        Returns:
            ParsedCVData object with skills, experience, education, and contact info
        """
        doc = self.nlp(text)

        # Extract all components
        skills = self._extract_skills(text, doc)
        contact = self._extract_contact(text, doc)
        experience = self._extract_experience(text, doc)
        education = self._extract_education(text, doc)

        return ParsedCVData(
            skills=skills, experience=experience, education=education, contact=contact
        )

    def _extract_skills(self, text: str, doc) -> List[str]:
        """Extract technical and professional skills"""
        skills = set()

        # Method 1: Match against known technical skills
        text_lower = text.lower()
        for skill in self.technical_skills:
            if skill in text_lower:
                skills.add(skill.title())

        # Method 2: Extract from "Skills" section using NER
        lines = text.split("\n")
        in_skills_section = False

        for line in lines:
            line_lower = line.lower().strip()

            # Detect skills section
            if any(
                header in line_lower
                for header in ["skill", "technical", "competenc", "technolog"]
            ):
                in_skills_section = True
                continue

            # Exit skills section on next major heading
            if (
                in_skills_section
                and line_lower
                and (
                    line_lower.startswith("experience")
                    or line_lower.startswith("education")
                    or line_lower.startswith("project")
                )
            ):
                in_skills_section = False

            # Extract from skills section
            if in_skills_section and line.strip():
                # Split by common delimiters
                potential_skills = re.split(r"[,;|•·]", line)
                for skill in potential_skills:
                    skill = skill.strip()
                    if skill and len(skill) > 1 and len(skill) < 30:
                        skills.add(skill)

        # Method 3: Use spaCy entities (ORG, PRODUCT for tools/technologies)
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG"] and len(ent.text) < 30:
                # Filter out obvious non-skills
                if not any(
                    word in ent.text.lower()
                    for word in ["university", "college", "company", "inc", "ltd"]
                ):
                    skills.add(ent.text.strip())

        return sorted(list(skills))[:30]  # Limit to 30 skills

    def _extract_contact(self, text: str, doc) -> Optional[ContactInfo]:
        """Extract contact information"""
        contact = ContactInfo()

        # Extract name (usually first line or PERSON entity)
        lines = text.split("\n")
        if lines:
            # First non-empty line is often the name
            first_line = lines[0].strip()
            if (
                first_line
                and len(first_line) < 50
                and not first_line.lower().startswith(("resume", "cv", "curriculum"))
            ):
                contact.name = first_line

        # Use NER for person names if not found
        if not contact.name:
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    contact.name = ent.text
                    break

        # Extract email
        email_match = self.email_pattern.search(text)
        if email_match:
            contact.email = email_match.group(0)

        # Extract phone
        phone_match = self.phone_pattern.search(text)
        if phone_match:
            contact.phone = phone_match.group(0)

        # Extract LinkedIn
        linkedin_match = self.linkedin_pattern.search(text)
        if linkedin_match:
            contact.linkedin = linkedin_match.group(0)

        # Extract location (look for GPE entities)
        for ent in doc.ents:
            if ent.label_ == "GPE" and not contact.location:
                contact.location = ent.text
                break

        return contact if any([contact.name, contact.email, contact.phone]) else None

    def _extract_experience(self, text: str, doc) -> List[Experience]:
        """Extract work experience entries"""
        experiences = []
        lines = text.split("\n")
        in_experience_section = False
        current_exp = None

        for i, line in enumerate(lines):
            line_stripped = line.strip()
            line_lower = line_stripped.lower()

            # Detect experience section
            if any(
                header in line_lower
                for header in ["experience", "employment", "work history"]
            ):
                in_experience_section = True
                continue

            # Exit experience section
            if in_experience_section and any(
                header in line_lower
                for header in ["education", "skill", "project", "certification"]
            ):
                if current_exp:
                    experiences.append(current_exp)
                break

            if in_experience_section and line_stripped:
                # Detect job title (usually has company name with | or - or at)
                if (
                    "|" in line_stripped
                    or " - " in line_stripped
                    or " at " in line_lower
                ):
                    # Save previous experience
                    if current_exp:
                        experiences.append(current_exp)

                    # Parse new experience entry
                    parts = re.split(r"(?i)\s+[|\-–]\s+|\s+at\s+", line_stripped)
                    if len(parts) >= 2:
                        current_exp = Experience(
                            title=parts[0].strip(),
                            company=parts[1].strip(),
                            duration="",
                            description="",
                        )

                # Extract dates (YYYY or Month YYYY format)
                elif current_exp and re.search(
                    r"\b(19|20)\d{2}\b|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
                    line_stripped,
                ):
                    current_exp.duration = line_stripped

                # Accumulate description (bullet points or regular lines)
                elif current_exp and line_stripped.startswith(("•", "-", "*", "–")):
                    if current_exp.description:
                        current_exp.description += "\n" + line_stripped
                    else:
                        current_exp.description = line_stripped

        # Add last experience
        if current_exp:
            experiences.append(current_exp)

        return experiences[:5]  # Limit to 5 most recent positions

    def _extract_education(self, text: str, doc) -> List[Education]:
        """Extract education entries"""
        educations = []
        lines = text.split("\n")
        in_education_section = False
        current_edu = None

        for line in lines:
            line_stripped = line.strip()
            line_lower = line_stripped.lower()

            # Detect education section
            if any(
                header in line_lower
                for header in ["education", "academic", "qualification"]
            ):
                in_education_section = True
                continue

            # Exit education section
            if in_education_section and any(
                header in line_lower
                for header in ["experience", "skill", "project", "certification"]
            ):
                if current_edu:
                    educations.append(current_edu)
                break

            if in_education_section and line_stripped:
                # Detect degree keywords
                if any(
                    degree in line_lower
                    for degree in [
                        "bachelor",
                        "master",
                        "phd",
                        "b.s.",
                        "m.s.",
                        "b.a.",
                        "m.a.",
                        "degree",
                    ]
                ):
                    # Save previous education
                    if current_edu:
                        educations.append(current_edu)

                    # Parse degree and institution
                    parts = re.split(
                        r"(?i)\s+[|\-–]\s+|\s+from\s+|\s+at\s+", line_stripped
                    )
                    degree_text = parts[0].strip()
                    institution_text = parts[1].strip() if len(parts) > 1 else ""

                    current_edu = Education(
                        degree=degree_text, institution=institution_text, year=""
                    )

                # Extract year
                elif current_edu:
                    year_match = re.search(r"\b(19|20)\d{2}\b", line_stripped)
                    year_match = re.search(r"\b(19|20)\d{2}\b", line_stripped)
                    if year_match and not current_edu.year:
                        current_edu.year = year_match.group(0)
                    elif not current_edu.institution:
                        current_edu.institution = line_stripped

        # Add last education
        if current_edu:
            educations.append(current_edu)

        return educations[:3]  # Limit to 3 degrees


# Create singleton instance (loaded once, shared across requests)
cv_parser = CVParser()
