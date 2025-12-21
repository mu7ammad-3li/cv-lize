"""
OpenRouter AI service for CV analysis and optimization
Using NVIDIA Nemotron 3 Nano 30B A3B model
"""

import json
import os
from typing import Dict

from models.schemas import CVAnalysis, OptimizedCV, ParsedCVData
from openai import AsyncOpenAI


class OpenRouterAnalyzer:
    """Analyze CVs using OpenRouter AI with NVIDIA Nemotron model"""

    def __init__(self):
        """Initialize OpenRouter API"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        model = os.getenv("OPENROUTER_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct")

        if not api_key:
            print("⚠️  OPENROUTER_API_KEY not set. CV analysis will not work.")
            self.client = None
            self.model = None
        else:
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            self.model = model
            print(f"✅ OpenRouter API initialized with model: {model}")

    async def analyze_cv(
        self, cv_data: ParsedCVData, cv_text: str, job_description: str
    ) -> Dict:
        """
        Analyze CV against job description

        Args:
            cv_data: Parsed CV data from spaCy
            cv_text: Raw CV text
            job_description: Target job description

        Returns:
            Dictionary with analysis and optimized CV
        """
        if not self.client:
            raise ValueError(
                "OpenRouter API not configured. Set OPENROUTER_API_KEY environment variable."
            )

        # Create prompt
        prompt = self._create_analysis_prompt(cv_data, cv_text, job_description)

        try:
            # Call OpenRouter API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert CV/resume analyzer and career coach with deep knowledge of ATS systems and hiring practices. Always respond with valid JSON only.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=16000,
            )

            # Parse response
            result_text = response.choices[0].message.content

            # Remove markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif result_text.startswith("```"):
                result_text = result_text.split("```")[1].split("```")[0].strip()

            try:
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse OpenRouter response: {e}")
                print(f"Raw response: {result_text[:500]}")
                # Return fallback response
                return self._create_fallback_response(cv_data)

        except Exception as e:
            print(f"❌ OpenRouter API error: {e}")
            return self._create_fallback_response(cv_data)

    def _create_analysis_prompt(
        self, cv_data: ParsedCVData, cv_text: str, job_description: str
    ) -> str:
        """Create detailed prompt for OpenRouter"""

        skills_list = ", ".join(cv_data.skills) if cv_data.skills else "None detected"
        exp_count = len(cv_data.experience) if cv_data.experience else 0
        edu_count = len(cv_data.education) if cv_data.education else 0

        prompt = f"""**Candidate's CV (Full Text):**
{cv_text[:10000]}

**Parsed Information:**
- Skills: {skills_list}
- Work Experience: {exp_count} position(s)
- Education: {edu_count} qualification(s)
- Contact: {cv_data.contact.name if cv_data.contact and cv_data.contact.name else "Not detected"}

**Target Job Description:**
{job_description[:5000]}

**Your Task:**
Analyze the CV against the job description and provide:

1. **Overall CV Score (0-100)**: Rate the CV quality considering formatting, content, and completeness
2. **Key Strengths (3-5 points)**: What makes this CV stand out
3. **Weaknesses or Gaps (3-5 points)**: Areas that need improvement
4. **Specific Suggestions (5-7 actionable items)**: Concrete improvements the candidate can make
5. **ATS Compatibility Score (0-100)**: How well will this CV pass through Applicant Tracking Systems
6. **Match Percentage (0-100)**: How well does the CV match the job requirements

**Then generate an optimized CV in markdown format** that:
- Highlights skills and experience relevant to the job description
- Reframes achievements to match job requirements
- Uses ATS-friendly formatting (clear headers, bullet points, no tables/graphics)
- Maintains a clean, professional Standard Resume structure
- Includes all original information but reorganized for maximum impact

**IMPORTANT**: Return ONLY valid JSON in this exact format (no additional text):

{{
  "score": 85,
  "strengths": [
    "Strong technical background in relevant technologies",
    "Clear demonstration of impact with quantifiable results",
    "Well-organized and easy to read"
  ],
  "weaknesses": [
    "Missing keywords from job description",
    "Lacks specific metrics in some roles",
    "Could emphasize leadership experience more"
  ],
  "suggestions": [
    "Add specific technologies mentioned in job posting (e.g., Kubernetes, CI/CD)",
    "Quantify achievements with numbers (e.g., 'Improved performance by 40%')",
    "Include a Professional Summary section at the top",
    "Highlight team collaboration and leadership experiences",
    "Add relevant certifications if any",
    "Use action verbs to start bullet points",
    "Tailor skills section to match job requirements"
  ],
  "atsCompatibility": 90,
  "matchPercentage": 75,
  "optimizedCV": "# Full Name\\n\\n## Contact Information\\n- Email: email@example.com\\n- Phone: +1234567890\\n- LinkedIn: linkedin.com/in/username\\n- Location: City, Country\\n\\n## Professional Summary\\nExperienced professional with X years in [field], specializing in [key skills from job description].\\n\\n## Skills\\n**Technical Skills**: Skill1, Skill2, Skill3\\n**Soft Skills**: Skill4, Skill5\\n\\n## Work Experience\\n\\n### Job Title | Company Name\\n*Start Date - End Date*\\n\\n- Achievement with quantifiable impact aligned to job requirements\\n- Responsibility demonstrating relevant skills\\n- Project outcome showing value delivered\\n\\n## Education\\n\\n### Degree in Field | Institution\\n*Year*\\n- Relevant details"
}}
"""

        return prompt

    def _create_fallback_response(self, cv_data: ParsedCVData) -> Dict:
        """Create fallback response if OpenRouter fails"""
        return {
            "score": 70,
            "strengths": [
                "CV structure is present",
                f"Contains {len(cv_data.skills)} identified skills",
                "Contact information detected",
            ],
            "weaknesses": [
                "Unable to perform detailed analysis at this time",
                "Please try again or check API limits",
            ],
            "suggestions": [
                "Ensure all sections are clearly labeled (Experience, Education, Skills)",
                "Use bullet points for achievements",
                "Include quantifiable metrics where possible",
                "Add relevant keywords from the job description",
                "Keep formatting simple and ATS-friendly",
            ],
            "atsCompatibility": 75,
            "matchPercentage": 60,
            "optimizedCV": f"# {cv_data.contact.name if cv_data.contact and cv_data.contact.name else 'Your Name'}\\n\\n## Skills\\n"
            + "\\n".join([f"- {skill}" for skill in cv_data.skills[:10]])
            + "\\n\\n*Optimized version will be generated with proper API access*",
        }


# Create singleton instance
openrouter_analyzer = OpenRouterAnalyzer()
