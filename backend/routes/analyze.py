"""
Analyze route for CV analysis using OpenRouter AI
"""

from fastapi import APIRouter, HTTPException, Request
from middleware.rate_limit import limiter
from models.database import get_cv_session, update_cv_session
from models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    CVAnalysis,
    CVSections,
    OptimizedCV,
    ParsedCVData,
    ParsedResumeData,
)
from services.keyword_analyzer import keyword_analyzer
from services.markdown_parser import markdown_parser
from services.openrouter_service import openrouter_analyzer

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
@limiter.limit("50/hour")  # 50 analysis requests per hour
async def analyze_cv(request: Request, analyze_request: AnalyzeRequest):
    """
    Analyze CV against job description using OpenRouter AI

    Steps:
    1. Fetch session from database
    2. Call OpenRouter AI with CV + job description
    3. Parse analysis results
    4. Generate optimized CV
    5. Update session in database
    6. Return analysis and optimized CV
    """

    # Fetch session
    session = await get_cv_session(analyze_request.session_id)

    if not session:
        raise HTTPException(
            status_code=404, detail=f"Session {analyze_request.session_id} not found"
        )

    # Check if session already has analysis (caching)
    if (
        session.get("analysis")
        and session.get("job_description") == analyze_request.job_description
    ):
        print(f"📦 Returning cached analysis for session {analyze_request.session_id}")

        # Parse the optimized CV markdown for display
        parsed_resume = None
        if session.get("optimized_cv") and session["optimized_cv"].get("markdown"):
            try:
                parsed_resume_data = markdown_parser.parse_markdown(
                    session["optimized_cv"]["markdown"]
                )
                parsed_resume = ParsedResumeData(**parsed_resume_data)
            except Exception as e:
                print(f"⚠️  Warning: Failed to parse markdown for cached session: {e}")

        return AnalyzeResponse(
            analysis=CVAnalysis(**session["analysis"]),
            optimized_cv=OptimizedCV(**session["optimized_cv"]),
            parsed_resume=parsed_resume,
        )

    # Get parsed data
    parsed_data_dict = session.get("parsed_data")
    if not parsed_data_dict:
        raise HTTPException(
            status_code=400,
            detail="CV has not been parsed yet. Please upload a CV first.",
        )

    parsed_data = ParsedCVData(**parsed_data_dict)

    # Get CV text
    cv_text = session.get("extracted_text")
    if not cv_text:
        raise HTTPException(status_code=400, detail="CV text not found in session")

    # Call OpenRouter AI
    try:
        print(
            f"🤖 Analyzing CV with OpenRouter AI for session {analyze_request.session_id}"
        )
        result = await openrouter_analyzer.analyze_cv(
            cv_data=parsed_data,
            cv_text=cv_text,
            job_description=analyze_request.job_description,
        )
    except Exception as e:
        print(f"❌ OpenRouter API error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze CV: {str(e)}")

    # Perform keyword analysis
    keyword_analysis_list = []
    missing_keywords_list = []
    semantic_similarity = 0.0

    try:
        print(f"🔍 Performing keyword analysis...")
        keyword_analysis_list = keyword_analyzer.analyze_keywords(
            cv_text, analyze_request.job_description
        )
        missing_keywords_list = keyword_analyzer.find_missing_keywords(
            cv_text, analyze_request.job_description
        )
        semantic_similarity = keyword_analyzer.calculate_semantic_similarity(
            cv_text, analyze_request.job_description
        )

        print(f"   Found {len(keyword_analysis_list)} keywords in resume")
        print(f"   Missing {len(missing_keywords_list)} critical keywords from JD")
        print(f"   Semantic similarity: {semantic_similarity:.2f}")
    except Exception as e:
        print(f"⚠️  Warning: Keyword analysis failed: {e}")

    # Parse result
    try:
        analysis = CVAnalysis(
            score=result.get("score", 70),
            strengths=result.get("strengths", []),
            weaknesses=result.get("weaknesses", []),
            suggestions=result.get("suggestions", []),
            ats_compatibility=result.get("atsCompatibility", 75),
            match_percentage=result.get("matchPercentage", 60),
            missing_keywords=result.get("missing_keywords", missing_keywords_list),
            keyword_analysis=result.get("keyword_analysis", keyword_analysis_list),
            formatting_issues=result.get("formatting_issues", []),
            semantic_similarity_score=result.get(
                "semantic_similarity_score", semantic_similarity
            ),
        )

        markdown_cv = result.get("optimizedCV", "# Optimized CV\n\nGeneration failed.")

        # Parse sections and subsections from the markdown
        sections_data = None
        try:
            parsed_sections = markdown_parser.parse_sections(markdown_cv)
            sections_data = CVSections(**parsed_sections)
            print(
                f"📋 Parsed {sections_data.total_sections} sections from optimized CV"
            )
        except Exception as e:
            print(f"⚠️  Warning: Failed to parse CV sections: {e}")

        optimized_cv = OptimizedCV(
            markdown=markdown_cv,
            sections=sections_data,
        )
    except Exception as e:
        print(f"⚠️  Warning: Failed to parse OpenRouter response: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to parse AI response. Please try again."
        )

    # Parse the optimized CV markdown for display (moved from frontend)
    parsed_resume = None
    try:
        parsed_resume_data = markdown_parser.parse_markdown(optimized_cv.markdown)
        parsed_resume = ParsedResumeData(**parsed_resume_data)
        print(f"📄 Parsed optimized CV markdown for professional display")
    except Exception as e:
        print(f"⚠️  Warning: Failed to parse optimized CV markdown: {e}")
        # Continue without parsed data - frontend can handle raw markdown

    # Update session in database
    await update_cv_session(
        analyze_request.session_id,
        {
            "job_description": analyze_request.job_description,
            "analysis": analysis.dict(),
            "optimized_cv": optimized_cv.dict(),
            "parsed_resume": parsed_resume.dict() if parsed_resume else None,
        },
    )

    print(f"✅ Analysis completed for session {analyze_request.session_id}")
    print(f"   Score: {analysis.score}/100")
    print(f"   ATS Compatibility: {analysis.ats_compatibility}/100")
    print(f"   Match: {analysis.match_percentage}%")

    return AnalyzeResponse(
        analysis=analysis,
        optimized_cv=optimized_cv,
        parsed_resume=parsed_resume,
    )
