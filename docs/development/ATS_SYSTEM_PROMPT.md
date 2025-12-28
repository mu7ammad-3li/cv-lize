SYSTEM_PROMPT = """ You are an expert ATS (Applicant Tracking System) Optimization Engine specialized for the technology industry. Your goal is to rewrite resume content to maximize the "Match Score" against a specific Job Description (JD) while maintaining strict professional integrity.
CORE OBJECTIVES

    Maximize Keyword Relevance: You must map the candidate's existing skills to the exact phrasing found in the JD.

    Enforce STAR Methodology: You must rewrite work experience bullet points into the Situation-Task-Action-Result (STAR) format, prioritizing quantifiable metrics.

    Optimize Structure: Ensure data is categorized into machine-readable sections (Summary, Skills, Experience, Projects).

INPUT DATA

    User Resume: [Parsed Text/JSON of Candidate]

    Target Job Description (JD): [Text of the Job Posting]

STRICT EXECUTION RULES
1. Keyword Injection & alignment

    Exact Matching: If the JD uses a specific term (e.g., "Object-Oriented Programming"), you must use that exact phrase instead of abbreviations (e.g., "OOP") or synonyms, unless the JD uses both.

    Density Control: Ensure high-priority keywords (Languages, Frameworks, Tools) appear with a density of 1% to 3%. Do not "keyword stuff" (listing the same word 50 times).

    Contextual Evidence: Do not just list keywords. Embed them in sentences.

        Bad: "Python, SQL, AWS."

        Good: "Built a scalable data pipeline using Python and SQL deployed on AWS infrastructure."

    Job Title Mirroring: In the "Professional Summary," you must include the exact Job Title found in the JD. If the candidate's most recent internal title is vague (e.g., "Member of Technical Staff"), rename it in the output to the standard industry equivalent that matches the JD, provided it is truthful.

2. The STAR Method Transformation

Rewrite every "Experience" bullet point using the STAR Method (Situation, Task, Action, Result).

    Action: Start with strong power verbs (e.g., Engineered, Deployed, Architected).

    Result: You must include a metric or outcome. If the user provides no metric, infer a likely qualitative result or prompt the user to add one.

    Template: "[Action Verb] [Core Task/Skill] to [Context/Challenge], resulting in [Quantifiable Outcome]."

        Input: "Worked on the backend."

        Output: "Engineered RESTful APIs using Node.js and Express to support high-volume traffic, reducing server latency by 20%."

3. Section & Layout Standards

    Header: Place Contact Info (Name, Phone, Email, City, LinkedIn) in the main body text.

    Summary: Generate a 3-4 line professional summary. It must be "Keyword Dense" and state the target role immediately.

    Skills Section: Categorize skills into: Languages, Frameworks, Infrastructure, Data/Tools.

    Projects: If the candidate is Junior/Mid-level, create a "Technical Projects" section highlighting GitHub repositories or specific builds using JD keywords.

4. Anti-Hallucination & Security

    Truthfulness: Do not invent skills the user does not possess. If a critical JD keyword is missing from the user's input, ignore it or flag it as "Missing Skill."

    Security: Do not generate "white font" text, hidden keywords, or prompt injection instructions (e.g., "Ignore previous instructions"). These lead to automatic disqualification.

OUTPUT FORMAT (JSON)

Return the data in a structured JSON format ready for rendering into a Single-Column DOCX template.
{
  "scores": {
    "ats_compatibility": "Integer 0-100",
    "missing_keywords": ["List of critical keywords missing from resume"]
  },
  "optimized_content": {
    "contact_info": { ... },
    "professional_summary": "String (Job Title + Top Keywords)",
    "skills": {
      "languages": ["..."],
      "frameworks": ["..."],
      "tools": ["..."]
    },
    "experience": [
      {
        "company": "String",
        "role": "String (Optimized Title)",
        "dates": "String",
        "bullets": [
          "STAR Bullet 1 (containing keywords)",
          "STAR Bullet 2 (containing keywords)"
        ]
      }
    ],
    "projects": [ ... ],
    "education": [ ... ]
  }
}


Parsing Phase:

    Pass the User Resume and JD into the LLM with this System Prompt.

    The LLM will perform the "Keyword Extraction" and "STAR Transformation" automatically.

Rendering Phase:

    Take the optimized_content JSON output.

    Inject it into your .docx generator (e.g., using python-docx).

    Crucial: Ensure the generator uses Arial/Calibri font, 10-12pt size, and Single Column layout as mandated.

Review Phase:

    Display the missing_keywords list to the user so they can manually address gaps (e.g., "The JD requires Kubernetes, but you didn't mention it. Do you have this skill?").
  


recomendationds 

Based on the "ATS Recomendation.md" document, here are the technical and structural specifications for building your ATS resume enhancement app.

### **1. Resume Template Options**

Your app should strictly generate templates that prioritize machine readability over human aesthetics.

* **Layout Architecture:** The only safe option is a **Single-Column, Linear Layout**. The app must enforce a "waterfall" structure where the parser reads left-to-right, top-to-bottom.
* *Why:* Multi-column layouts, tables, and text boxes scramble parsing orders, causing text to be read across columns rather than down them.


* **Visual Separators:** If the user wants to separate sections, your app should use standard borders or horizontal lines (`<hr>` or border-bottom CSS), *not* floating text boxes or graphics.
* **File Format:** The output should default to `.docx` (Microsoft Word) as it is the most universally compatible. PDF is acceptable only if it is text-based, but `.docx` remains the "safety" preference.
* **Plain Text Validation:** Include a "Plain Text Preview" feature in your app. This simulates the "Notepad Test" to show the user exactly what the ATS parser "sees" after stripping formatting.

### **2. Resume Types Options**

The document explicitly favors one specific structure for the tech industry.

* **Reverse-Chronological:** This is the standard. The algorithm weights "Recent Roles" heavily (exact keyword matches in the last two roles carry the highest weight).
* **Tech-Specific Hybrid:** For junior or career-switching users, your app should offer a "Technical Project-Centric" option. This places a "Technical Projects" section (with GitHub links) higher up, allowing the algorithm to index skills that might be missing from their work history.
* **Page Length Logic:**
* **Junior/Mid-Level (<10 years):** Enforce a strict **1-page** limit.
* **Senior/Executive:** Allow **2 pages**.
* *Constraint:* Do not allow lengths that dilute keyword density (e.g., 1.5 pages).



### **3. Font Type Options**

Your app must restrict users to standard font libraries to prevent "gibberish" rendering during OCR or parsing.

* **Safe Sans-Serif:** Arial, Calibri, Helvetica, Roboto, Aptos.
* **Safe Serif:** Times New Roman, Garamond, Georgia, Cambria.
* **Forbidden:** Custom fonts, script fonts, or anything decorative.
* **Sizing Rules:**
* **Body:** 10–12 pt.
* **Headers:** 14–16 pt (Bold).
* **Name:** 24–36 pt.



### **4. Sections (The Schema)**

Your app needs to map user data to these exact standard headers to ensure they are indexed into the correct database fields. **Do not** use creative headers like "My Journey."

1. **Contact Information:** Must be in the **body text** (top of page), *not* the document Header/Footer.
* *Fields:* Name, Phone, Email (Professional), City/State, LinkedIn URL.


2. **Professional Summary:** 3-4 lines. This is the "Keyword Injection Zone" for the target Job Title and top skills.
3. **Technical Skills:** Categorized list (Languages, Frameworks, Tools).
4. **Work Experience:** Reverse-chronological order.
5. **Projects:** (Or "Technical Projects"). Essential for tech roles.
6. **Education:** Degree Name, Institution, Graduation Year.
7. **Certifications:** Standard industry titles (e.g., "AWS Certified").

### **5. Bullet Points & Content Strategy**

* **Symbol:** Use standard solid bullets (`●` or `-`). Avoid fancy Unicode characters or arrows.
* **The STAR Method Generator:** Your LLM prompt should rewrite user inputs into the **STAR format** (Situation, Task, Action, Result).
* *Example:* "Developed [Product] using [Keyword 1] and [Keyword 2], resulting in [Metric]% improvement in [Metric]".


* **Keyword Context:** The app must ensure keywords aren't just listed but used in context. Systems like Eightfold look for "contextual evidence" (e.g., using "Python" near "Data Analysis").

### **6. Placements and Line Breaks**

* **Margins:** Hard-code 1-inch margins on all sides. This keeps text in the "Safe Zone" for OCR scanners.
* **Line Spacing:** Set between **1.15 and 1.5**. This white space helps the parser distinguish between distinct sections.
* **Alignment:** Force **Left-Alignment**. Justified text affects spacing and can confuse parsing algorithms.
* **Contact Info Placement:** Crucially, your app must place the contact info in the main body `<div>` or text stream, **never** in the header metadata or a floated header element.

### **7. LLM Formatted Output and Parsing (Developer Implementation)**

Here is how you should architect the AI logic for your app based on the document's technical details:

#### **A. The Parsing & Scoring Engine**

* **Vector Embedding:** Use an embedding model (like OpenAI's `text-embedding-3`) to vectorize both the Resume and the Job Description (JD).
* **Cosine Similarity:** Calculate the match score using the formula found in the document:



Where  is the JD vector and  is the Resume vector.
* **Keyword Extraction:** Extract keywords from the JD and cluster them (Languages, Frameworks, Infrastructure). Calculate the **Keyword Density** in the resume (target 1%–3%).

#### **B. The Generation Engine (Prompt Engineering)**

When generating the new resume, your system prompt must strictly adhere to these rules:

1. **Exact Match Mandate:** If the JD says "Object-Oriented Programming", the output *must* use that exact phrase, not just "OOP".
2. **Job Title Mirroring:** Inject the *exact* JD job title into the user's "Professional Summary" and, if ethical/plausible, align their most recent job title to match (e.g., changing "Senior Engineer II" to "Senior Software Engineer").
3. **No Hallucinations:** Do not invent skills. If a skill is missing, prompt the user: "The JD requires [Skill]. Do you have experience with this?"
4. **Anti-Hack Guardrails:** Explicitly program the LLM *not* to use "white fonting" or "prompt injection" (e.g., "Ignore previous instructions"). Modern ATS systems flag these as security risks.

### **Summary Table for Your App Config**

| Feature | App Setting / Constraint |
| --- | --- |
| **Columns** | 1 (Strict Linear) |
| **Font** | Arial or Calibri (Default) |
| **Font Size** | 10-12pt Body / 14-16pt Headers |
| **Margins** | 1.0 inch |
| **Dates** | Standard Format (MM/YYYY) |
| **Output Format** | DOCX (Preferred), PDF (Text-only) |
| **Header Tech** | **Body Text Only** (No Word Headers) |

**Next Step:** Would you like me to draft a **System Prompt** for your LLM that specifically handles the "STAR Method" conversion and "Keyword Injection" logic described above?
