"""
Keyword extraction and density analysis for ATS optimization
"""

import re
from collections import Counter
from typing import Dict, List, Set, Tuple

import spacy
from models.schemas import KeywordAnalysis, MissingKeyword


class KeywordAnalyzer:
    """
    Analyze keywords for ATS optimization

    Features:
    - Extract technical keywords from resume and job description
    - Calculate keyword density (1-3% is optimal)
    - Identify missing critical keywords
    - Categorize keywords (languages, frameworks, tools, methodologies)
    - Extract contextual usage
    """

    # Technical keyword categories for tech industry
    KEYWORD_CATEGORIES = {
        "languages": [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "C#",
            "TypeScript",
            "Go",
            "Golang",
            "Ruby",
            "PHP",
            "Swift",
            "Kotlin",
            "Rust",
            "Scala",
            "R",
            "MATLAB",
            "SQL",
            "HTML",
            "CSS",
            "Bash",
            "Shell",
            "PowerShell",
        ],
        "frameworks": [
            "React",
            "React.js",
            "Angular",
            "Vue",
            "Vue.js",
            "Node.js",
            "Express",
            "Django",
            "Flask",
            "FastAPI",
            "Spring",
            "Spring Boot",
            ".NET",
            "ASP.NET",
            "Rails",
            "Ruby on Rails",
            "Laravel",
            "TensorFlow",
            "PyTorch",
            "Keras",
            "Scikit-learn",
            "Pandas",
            "NumPy",
            "Next.js",
            "Nuxt",
            "Svelte",
        ],
        "infrastructure": [
            "AWS",
            "Azure",
            "Google Cloud",
            "GCP",
            "Docker",
            "Kubernetes",
            "K8s",
            "Terraform",
            "Ansible",
            "Jenkins",
            "CircleCI",
            "GitLab CI",
            "GitHub Actions",
            "CI/CD",
            "DevOps",
            "CloudFormation",
            "Lambda",
            "EC2",
            "S3",
            "ECS",
            "EKS",
        ],
        "databases": [
            "MongoDB",
            "PostgreSQL",
            "MySQL",
            "SQL Server",
            "Oracle",
            "Redis",
            "Elasticsearch",
            "DynamoDB",
            "Cassandra",
            "Neo4j",
            "SQLite",
            "MariaDB",
            "NoSQL",
            "Relational Database",
            "Database",
        ],
        "tools": [
            "Git",
            "GitHub",
            "GitLab",
            "Bitbucket",
            "Jira",
            "Confluence",
            "Slack",
            "VS Code",
            "IntelliJ",
            "Eclipse",
            "Jupyter",
            "Tableau",
            "PowerBI",
            "Postman",
            "Swagger",
            "npm",
            "yarn",
            "pip",
            "Maven",
            "Gradle",
        ],
        "methodologies": [
            "Agile",
            "Scrum",
            "Kanban",
            "Waterfall",
            "DevOps",
            "CI/CD",
            "TDD",
            "Test-Driven Development",
            "BDD",
            "Microservices",
            "REST API",
            "RESTful",
            "GraphQL",
            "SOAP",
            "API",
            "Object-Oriented Programming",
            "OOP",
            "Functional Programming",
            "SDLC",
            "Software Development Life Cycle",
        ],
        "ai_ml": [
            "Machine Learning",
            "ML",
            "Deep Learning",
            "Neural Network",
            "NLP",
            "Natural Language Processing",
            "Computer Vision",
            "AI",
            "Artificial Intelligence",
            "Data Science",
            "Big Data",
            "Apache Spark",
            "Hadoop",
            "MLOps",
            "Model Deployment",
        ],
    }

    def __init__(self):
        """Initialize keyword analyzer with spaCy"""
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            print("⚠️  spaCy model 'en_core_web_md' not found. Using 'en_core_web_sm'")
            self.nlp = spacy.load("en_core_web_sm")

        # Build reverse lookup for categories
        self.keyword_to_category = {}
        for category, keywords in self.KEYWORD_CATEGORIES.items():
            for keyword in keywords:
                # Store both original and lowercase for matching
                self.keyword_to_category[keyword.lower()] = category

    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """
        Extract technical keywords from text

        Args:
            text: Resume or job description text

        Returns:
            Dictionary of keywords by category
        """
        keywords_by_category = {
            category: [] for category in self.KEYWORD_CATEGORIES.keys()
        }

        # Process text with spaCy
        doc = self.nlp(text)
        text_lower = text.lower()

        # Extract keywords from each category
        for category, keyword_list in self.KEYWORD_CATEGORIES.items():
            for keyword in keyword_list:
                # Case-insensitive search
                if keyword.lower() in text_lower:
                    keywords_by_category[category].append(keyword)

        # Also extract using NER for technologies
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG", "GPE"]:
                # Check if it might be a tech term
                if len(ent.text) > 2 and ent.text.isalnum():
                    # Try to categorize it
                    category = self.keyword_to_category.get(ent.text.lower(), "other")
                    if category != "other":
                        if ent.text not in keywords_by_category[category]:
                            keywords_by_category[category].append(ent.text)

        return keywords_by_category

    def calculate_keyword_density(self, text: str, keyword: str) -> Tuple[int, float]:
        """
        Calculate frequency and density of a keyword

        Args:
            text: Text to analyze
            keyword: Keyword to count

        Returns:
            Tuple of (frequency, density_percentage)
        """
        # Case-insensitive search
        text_lower = text.lower()
        keyword_lower = keyword.lower()

        # Count occurrences
        frequency = text_lower.count(keyword_lower)

        # Calculate density (percentage)
        word_count = len(text.split())
        density = (frequency / word_count * 100) if word_count > 0 else 0.0

        return frequency, density

    def extract_keyword_context(
        self, text: str, keyword: str, max_contexts: int = 3
    ) -> List[str]:
        """
        Extract sentences containing the keyword

        Args:
            text: Text to analyze
            keyword: Keyword to find
            max_contexts: Maximum number of context sentences to return

        Returns:
            List of sentences containing the keyword
        """
        doc = self.nlp(text)
        contexts = []

        keyword_lower = keyword.lower()

        for sent in doc.sents:
            if keyword_lower in sent.text.lower() and len(contexts) < max_contexts:
                # Clean up sentence
                clean_sent = sent.text.strip()
                if clean_sent:
                    contexts.append(clean_sent)

        return contexts

    def analyze_keywords(self, resume_text: str, jd_text: str) -> List[KeywordAnalysis]:
        """
        Comprehensive keyword analysis

        Args:
            resume_text: Resume text
            jd_text: Job description text

        Returns:
            List of KeywordAnalysis objects
        """
        # Extract keywords from both texts
        resume_keywords = self.extract_keywords(resume_text)
        jd_keywords = self.extract_keywords(jd_text)

        # Analyze each keyword in resume
        analyses = []

        for category, keywords in resume_keywords.items():
            for keyword in keywords:
                # Calculate frequency and density
                frequency, density = self.calculate_keyword_density(
                    resume_text, keyword
                )

                # Check if in job description
                in_jd = any(
                    keyword.lower() == jd_kw.lower() for jd_kw in jd_keywords[category]
                )

                # Extract context
                context_usage = self.extract_keyword_context(
                    resume_text, keyword, max_contexts=2
                )

                # Create analysis
                analysis = KeywordAnalysis(
                    keyword=keyword,
                    frequency=frequency,
                    density=round(density, 2),
                    category=category,
                    in_jd=in_jd,
                    context_usage=context_usage,
                )

                analyses.append(analysis)

        # Sort by density (highest first)
        analyses.sort(key=lambda x: x.density, reverse=True)

        return analyses

    def find_missing_keywords(
        self, resume_text: str, jd_text: str
    ) -> List[MissingKeyword]:
        """
        Find critical keywords from JD missing in resume

        Args:
            resume_text: Resume text
            jd_text: Job description text

        Returns:
            List of MissingKeyword objects
        """
        # Extract keywords
        resume_keywords = self.extract_keywords(resume_text)
        jd_keywords = self.extract_keywords(jd_text)

        missing = []

        # Check each JD keyword category
        for category, jd_kw_list in jd_keywords.items():
            resume_kw_set = {kw.lower() for kw in resume_keywords.get(category, [])}

            for jd_keyword in jd_kw_list:
                if jd_keyword.lower() not in resume_kw_set:
                    # Determine importance based on frequency in JD
                    frequency, density = self.calculate_keyword_density(
                        jd_text, jd_keyword
                    )

                    # High frequency = high importance
                    if density > 1.0:
                        importance = "critical"
                    elif density > 0.5:
                        importance = "high"
                    elif density > 0.2:
                        importance = "medium"
                    else:
                        importance = "low"

                    # Generate suggestion
                    suggestion = self._generate_keyword_suggestion(jd_keyword, category)

                    missing_kw = MissingKeyword(
                        keyword=jd_keyword,
                        category=category,
                        importance=importance,
                        suggestion=suggestion,
                    )

                    missing.append(missing_kw)

        # Sort by importance
        importance_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        missing.sort(key=lambda x: importance_order[x.importance])

        return missing

    def _generate_keyword_suggestion(self, keyword: str, category: str) -> str:
        """Generate a helpful suggestion for missing keyword"""

        suggestions = {
            "languages": f"Add {keyword} to your skills section if you have experience with this programming language. If not, consider learning it for this role.",
            "frameworks": f"Highlight any projects or work experience using {keyword}. If you haven't used it, consider building a sample project.",
            "infrastructure": f"Add {keyword} experience to your resume if you've worked with this platform. Cloud certifications can strengthen your profile.",
            "databases": f"Include {keyword} in your technical skills and mention specific use cases in your work experience.",
            "tools": f"List {keyword} in your tools section if you've used it. It's commonly used in this field.",
            "methodologies": f"Demonstrate {keyword} experience by describing how you've applied this methodology in past projects.",
            "ai_ml": f"Add {keyword} to your skills and showcase relevant projects or research. This is a key requirement for the role.",
        }

        return suggestions.get(
            category,
            f"Consider adding {keyword} to your resume if you have relevant experience.",
        )

    def calculate_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Calculate semantic similarity between resume and job description

        Uses spaCy's word vectors for cosine similarity

        Args:
            resume_text: Resume text
            jd_text: Job description text

        Returns:
            Similarity score (0.0 to 1.0)
        """
        try:
            # Process texts
            resume_doc = self.nlp(resume_text[:10000])  # Limit length
            jd_doc = self.nlp(jd_text[:5000])

            # Calculate similarity
            similarity = resume_doc.similarity(jd_doc)

            return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]

        except Exception as e:
            print(f"⚠️  Semantic similarity calculation failed: {e}")
            return 0.0


# Create singleton instance
keyword_analyzer = KeywordAnalyzer()
