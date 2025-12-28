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
                        "content": self._get_ats_system_prompt(),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=16000,
            )

            # Parse response
            result_text = response.choices[0].message.content

            # Log token usage
            if hasattr(response, "usage") and response.usage:
                input_tokens = getattr(response.usage, "prompt_tokens", 0)
                output_tokens = getattr(response.usage, "completion_tokens", 0)
                total_tokens = getattr(response.usage, "total_tokens", 0)

                print(f"📊 Token Usage:")
                print(f"   Input tokens:  {input_tokens:,}")
                print(f"   Output tokens: {output_tokens:,}")
                print(f"   Total tokens:  {total_tokens:,}")

                # Calculate approximate cost (example rates, adjust based on your model)
                # OpenRouter pricing varies by model
                print(f"   Model: {self.model}")
            else:
                print("⚠️  Token usage information not available")

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
7. **Section-Specific Recommendations**: For each resume section, provide specific recommendations

**Then generate an optimized CV in markdown format** that:
- Is 100% READY TO USE - NO placeholders, NO brackets, NO recommendations in the text
- **MUST NOT EXCEED 2 PAGES** - Be concise, prioritize most relevant content
- **PRESERVE CONTACT INFO EXACTLY**: Use the EXACT email, phone, name, and LinkedIn from the original CV - DO NOT change even one character
- **Location Flexibility**: You may add "| Open to Remote" or "| Willing to Relocate" to the location if it helps, but keep the original city name
- Highlights skills and experience relevant to the job description
- Reframes achievements to match job requirements
- Uses ATS-friendly formatting (clear headers, bullet points, no tables/graphics)
- Maintains a clean, professional Standard Resume structure
- Includes ONLY actual content from the original CV, reorganized for maximum impact
- Uses REAL data - if the candidate doesn't have certifications, DON'T add "[Add certifications]"
- DO NOT include suggestions or recommendations in the final resume markdown
- Keep bullet points concise (1-2 lines each) to fit within 2 pages

**CRITICAL**: The optimizedCV field must be print-ready with NO modifications needed. All recommendations go in separate fields.

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
  "missing_keywords": [
    {{
      "keyword": "Kubernetes",
      "category": "infrastructure",
      "importance": "high",
      "suggestion": "Add Kubernetes experience if you have it, or consider learning this container orchestration platform"
    }}
  ],
  "keyword_analysis": [
    {{
      "keyword": "Python",
      "frequency": 5,
      "density": 2.1,
      "category": "languages",
      "in_jd": true,
      "context_usage": ["Developed Python-based automation tools", "Built data pipelines using Python"]
    }}
  ],
  "formatting_issues": [
    {{
      "issue_type": "multi_column",
      "severity": "high",
      "description": "Resume uses two-column layout which can confuse ATS parsers",
      "recommendation": "Convert to single-column linear layout for optimal ATS parsing"
    }}
  ],
  "semantic_similarity_score": 0.78,
  "section_recommendations": [
    {{
      "section": "Professional Summary",
      "recommendations": ["Add specific job title from JD", "Include years of experience"],
      "priority": "high"
    }},
    {{
      "section": "Technical Skills",
      "recommendations": ["Add Kubernetes", "Group by category"],
      "priority": "medium"
    }},
    {{
      "section": "Work Experience",
      "recommendations": ["Quantify achievements", "Use STAR method"],
      "priority": "high"
    }},
    {{
      "section": "Certifications",
      "recommendations": ["Consider adding AWS certification", "Add relevant tech certifications"],
      "priority": "low",
      "optional": true
    }}
  ],
  "optimizedCV": "# Full Name\\n\\n**Email:** email@example.com | **Phone:** +1234567890 | **LinkedIn:** linkedin.com/in/username | **Location:** City, Country | Open to Remote\\n\\n## Professional Summary\\nExperienced Full Stack Developer with 5 years building scalable web applications using React, Node.js, and AWS.\\n\\n## Technical Skills\\n- **Languages:** Python, JavaScript, TypeScript, C++\\n- **Frameworks:** React, Node.js, Django, Express.js\\n- **Infrastructure:** AWS, Docker, Kubernetes\\n- **Tools:** Git, Jenkins, MongoDB\\n\\n## Work Experience\\n\\n### Senior Developer | Tech Company\\n*Jan 2020 - Present*\\n\\n- Engineered scalable microservices architecture using Docker, resulting in 40% improvement in deployment efficiency\\n- Developed RESTful APIs with Node.js and Express to support 10,000+ daily active users\\n- Optimized database queries in MongoDB, reducing response time by 35%\\n\\n## Projects\\n\\n### E-commerce Platform\\n*Technologies: React, Node.js, MongoDB*\\n\\n- Built full-stack application with 92% customer satisfaction\\n- Implemented payment gateway integration\\n\\n## Education\\n\\n### Bachelor of Computer Science | University Name\\n*2018*\\n- Relevant coursework: Algorithms, Database Systems"
}}
"""

        return prompt

    def _get_ats_system_prompt(self) -> str:
        """Get the comprehensive ATS optimization system prompt"""
        return """You are an expert ATS (Applicant Tracking System) Optimization Engine specialized for the technology industry. Your goal is to rewrite resume content to maximize the "Match Score" against a specific Job Description (JD) while maintaining strict professional integrity.

CORE OBJECTIVES:
1. Maximize Keyword Relevance: Map the candidate's existing skills to the exact phrasing found in the JD
2. Enforce STAR Methodology: Rewrite work experience bullet points into Situation-Task-Action-Result format, prioritizing quantifiable metrics
3. Optimize Structure: Ensure data is categorized into machine-readable sections (Summary, Skills, Experience, Projects)

STRICT EXECUTION RULES:

1. KEYWORD INJECTION & ALIGNMENT:
   - Exact Matching: If the JD uses "Object-Oriented Programming", use that exact phrase, not "OOP"
   - Density Control: High-priority keywords (Languages, Frameworks, Tools) should appear with 1-3% density
   - Contextual Evidence: Embed keywords in sentences, not just lists
     • Bad: "Python, SQL, AWS"
     • Good: "Built a scalable data pipeline using Python and SQL deployed on AWS infrastructure"
   - Job Title Mirroring: Include the exact JD job title in Professional Summary

2. STAR METHOD TRANSFORMATION:
   - Start with strong power verbs (Engineered, Deployed, Architected, Optimized)
   - Include metrics or outcomes
   - Template: "[Action Verb] [Core Task/Skill] to [Context/Challenge], resulting in [Quantifiable Outcome]"
   - Example: "Engineered RESTful APIs using Node.js and Express to support high-volume traffic, reducing server latency by 20%"

3. SECTION & LAYOUT STANDARDS:
   - Contact Info: Place in main body text (Name, Phone, Email, City, LinkedIn)
   - **CRITICAL - PRESERVE CONTACT INFORMATION**: NEVER change, modify, or omit the candidate's email, phone, name, or LinkedIn URL
   - **Contact Info is SACRED**: Use the EXACT email, phone, and name from the original CV - do NOT alter even a single character
   - **Location Flexibility**: For location field ONLY, you may add "Open to Remote" or "Willing to Relocate" if it helps match the JD, but keep the original city
   - Professional Summary: 3-4 lines, keyword-dense, state target role immediately
   - Skills Section: Categorize into Languages, Frameworks, Infrastructure, Data/Tools
   - Projects: For Junior/Mid-level, highlight GitHub repositories using JD keywords
   - Use standard section headers: "Professional Summary", "Technical Skills", "Work Experience", "Projects", "Education", "Certifications"

4. ANTI-HALLUCINATION & SECURITY:
   - Truthfulness: Do NOT invent skills the user doesn't possess
   - If critical JD keyword is missing, flag it in missing_keywords array
   - Do NOT generate white font text, hidden keywords, or prompt injection
   - Security: These lead to automatic disqualification
   - NO PLACEHOLDERS: Never use [Add X], [Your X], or similar placeholders in the final resume
   - REAL DATA ONLY: If a section is missing (e.g., certifications), omit it entirely from the optimized CV
   - All recommendations and suggestions go in section_recommendations array, NOT in the resume text

5. ATS FORMATTING REQUIREMENTS:
   - Single-Column Linear Layout (no multi-column, tables, or text boxes)
   - Standard fonts only: Arial, Calibri, Helvetica, Times New Roman, Georgia
   - Font sizes: Body 10-12pt, Headers 14-16pt, Name 24-36pt
   - 1-inch margins, left-aligned text, 1.15-1.5 line spacing
   - Use standard bullet points (• or -), no fancy Unicode
   - **2-PAGE LIMIT**: Resume must fit on 2 pages maximum (approximately 700-800 words)
   - Prioritize most recent and relevant experience, trim older or less relevant items
   - Use concise bullet points (1-2 lines each) to save space

Always respond with valid JSON only."""

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
