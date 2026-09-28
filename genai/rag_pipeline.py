import json
import requests

from .schemas import RAGAnalysisResult
from .education_extractor import extract_education
from .experience_extractor import extract_experience_evidence


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def build_grounded_prompt(
    resume_context,
    job_description,
    matching_skills,
    missing_skills,
    experience_evidence,
):
    """
    Build a grounded prompt using retrieved resume evidence
    and deterministic experience extraction.
    """

    prompt = f"""
You are an AI resume-job matching assistant.

Analyze the candidate's resume against the job description.

The information supplied below comes from deterministic
processing of the candidate's resume.

Use it as the source of truth.

========================
JOB DESCRIPTION
========================

{job_description}


========================
RETRIEVED RESUME EVIDENCE
========================

{resume_context}


========================
DETERMINISTIC EXPERIENCE EVIDENCE
========================

{experience_evidence}


========================
DETERMINISTIC SKILL ANALYSIS
========================

Matching skills:
{matching_skills}

Missing skills:
{missing_skills}


========================
STRICT RULES
========================

1. Never invent information.

2. Do not invent:
   - employers
   - job titles
   - dates
   - projects
   - technologies
   - achievements
   - responsibilities
   - qualifications

3. The matching_skills list is deterministic.
   Do not change it.

4. The missing_skills list is deterministic.
   Do not change it.

5. The experience evidence was extracted
   deterministically from the resume.

6. Do not invent additional experience.

7. Use the supplied experience evidence to explain
   which experience is relevant to the job description.

8. Keep the meaning of the supplied experience evidence.
   Do not add unsupported details.

9. Recommendations should focus primarily on
   the missing skills.

10. Do not recommend a skill that is already present
    in the matching_skills list.

11. Do not claim the candidate has experience with
    a missing skill.

12. Return ONLY valid JSON.

13. relevant_experience MUST be a list of strings.

14. recommendations MUST be a list of strings.


========================
OUTPUT FORMAT
========================

{{
    "relevant_experience": [],
    "recommendations": []
}}
"""

    return prompt


def call_ollama(prompt):
    """
    Send the grounded prompt to the local Ollama model.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]


def run_rag_analysis(
    resume_context,
    job_description,
    matching_skills,
    missing_skills,
):
    """
    Run the complete RAG analysis.

    Deterministic components:
        - experience evidence
        - education
        - matching skills
        - missing skills

    LLM component:
        - explanation of relevant experience
        - recommendations

    Pydantic:
        - final structure validation
    """

    # -----------------------------------------
    # 1. Deterministic experience extraction
    # -----------------------------------------

    experience_evidence = extract_experience_evidence(
        resume_context
    )

    # -----------------------------------------
    # 2. Deterministic education extraction
    # -----------------------------------------

    education = extract_education(
        resume_context
    )

    if education:
        education_alignment = "; ".join(
            education
        )
    else:
        education_alignment = (
            "Not found in the retrieved resume information."
        )

    # -----------------------------------------
    # 3. Build grounded LLM prompt
    # -----------------------------------------

    prompt = build_grounded_prompt(
        resume_context=resume_context,
        job_description=job_description,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        experience_evidence=experience_evidence,
    )

    # -----------------------------------------
    # 4. Call local Qwen model
    # -----------------------------------------

    raw_response = call_ollama(prompt)

    # -----------------------------------------
    # 5. Parse JSON
    # -----------------------------------------

    try:

        parsed_response = json.loads(
            raw_response
        )

    except json.JSONDecodeError:

        parsed_response = {
            "relevant_experience": [],
            "recommendations": [],
        }

    # -----------------------------------------
    # 6. Use deterministic experience evidence
    #    as fallback if Qwen misses it
    # -----------------------------------------

    llm_experience = parsed_response.get(
        "relevant_experience",
        []
    )

    if not llm_experience and experience_evidence:

        llm_experience = experience_evidence

    # -----------------------------------------
    # 7. Get recommendations
    # -----------------------------------------

    recommendations = parsed_response.get(
        "recommendations",
        []
    )

    # -----------------------------------------
    # 8. Validate final structure
    # -----------------------------------------

    validated_result = RAGAnalysisResult(
        relevant_experience=llm_experience,
        education_alignment=education_alignment,
        recommendations=recommendations,
    )

    return validated_result