"""
Pydantic models for data validation and serialization
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class FileType(str, Enum):
    PDF = "pdf"
    MARKDOWN = "markdown"
    TEXT = "txt"


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    location: Optional[str] = None


class Experience(BaseModel):
    title: str
    company: str
    duration: str
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Education(BaseModel):
    degree: str
    institution: str
    year: str
    gpa: Optional[str] = None
    honors: Optional[str] = None


class ParsedCVData(BaseModel):
    skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    contact: Optional[ContactInfo] = None


class CVAnalysis(BaseModel):
    score: int = Field(ge=0, le=100, description="Overall CV score")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    ats_compatibility: int = Field(
        ge=0, le=100, description="ATS compatibility score", default=75
    )
    match_percentage: int = Field(
        ge=0, le=100, description="Match with job description"
    )


class CVSubsection(BaseModel):
    """Subsection within a CV section"""

    title: str
    date: Optional[str] = None
    content: str
    paragraphs: List[str] = Field(default_factory=list)
    bullets: List[str] = Field(default_factory=list)


class CVSection(BaseModel):
    """Main section of a CV"""

    title: str
    content: str
    subsections: List[CVSubsection] = Field(default_factory=list)
    paragraphs: List[str] = Field(default_factory=list)
    bullets: List[str] = Field(default_factory=list)


class CVSections(BaseModel):
    """Structured sections from parsed markdown CV"""

    sections: List[CVSection] = Field(default_factory=list)
    total_sections: int = 0


class OptimizedCV(BaseModel):
    markdown: str
    sections: Optional[CVSections] = None


class CVSession(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    original_filename: str
    file_hash: str
    file_type: FileType
    extracted_text: str
    job_description: Optional[str] = None
    parsed_data: Optional[ParsedCVData] = None
    analysis: Optional[CVAnalysis] = None
    optimized_cv: Optional[OptimizedCV] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "original_filename": "john_doe_resume.pdf",
                "file_hash": "a1b2c3...",
                "file_type": "pdf",
                "extracted_text": "John Doe\nSoftware Engineer...",
                "job_description": "We are looking for...",
                "parsed_data": {
                    "skills": ["Python", "FastAPI", "MongoDB"],
                    "experience": [],
                    "education": [],
                    "contact": {"name": "John Doe", "email": "john@example.com"},
                },
                "analysis": {
                    "score": 85,
                    "strengths": ["Strong technical skills"],
                    "weaknesses": ["Lack of leadership experience"],
                    "suggestions": ["Add metrics to achievements"],
                    "ats_compatibility": 90,
                    "match_percentage": 78,
                },
                "optimized_cv": {"markdown": "# John Doe\n\n## Contact\n..."},
            }
        }


# Request/Response models
class UploadResponse(BaseModel):
    session_id: str
    filename: str
    file_hash: str
    extracted_text: str
    parsed_data: ParsedCVData


class AnalyzeRequest(BaseModel):
    session_id: str
    job_description: str = Field(..., min_length=10, description="Job description text")


class ParsedResumeData(BaseModel):
    """Structured resume data parsed from markdown"""

    personalInfo: Dict = Field(default_factory=dict)
    experience: List[Dict] = Field(default_factory=list)
    skills: Dict = Field(default_factory=dict)
    education: Dict = Field(default_factory=dict)
    certifications: List[str] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    analysis: CVAnalysis
    optimized_cv: OptimizedCV
    parsed_resume: Optional[ParsedResumeData] = None


class SessionResponse(BaseModel):
    session_id: str
    original_filename: str
    parsed_data: Optional[ParsedCVData]
    analysis: Optional[CVAnalysis]
    optimized_cv: Optional[OptimizedCV]
    created_at: datetime


class SecurityIssue(BaseModel):
    type: str
    severity: str
    message: str


class ValidationResponse(BaseModel):
    is_valid: bool
    issues: List[SecurityIssue] = Field(default_factory=list)
    risk_level: str
    file_hash: str
