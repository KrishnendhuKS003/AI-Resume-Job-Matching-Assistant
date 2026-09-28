from matching.hybrid_matcher import analyze_resume_job_match

from genai.retriever import ResumeRetriever
from genai.rag_pipeline import run_rag_analysis
from genai.recommendations import generate_recommendations
from genai.document_parser import extract_resume_text
from genai.education_extractor import extract_education
from genai.experience_extractor import extract_experience_evidence


def analyze_full_resume_job_match(
    resume_text,
    job_description,
    top_k=3,
    chunk_size=500
):
    """
    Run the complete resume-job matching pipeline.

    Experience and education are extracted directly from
    the full resume.

    The LLM is NOT allowed to create or rewrite experience.
    """

    resume_text = str(resume_text).strip()
    job_description = str(job_description).strip()

    if not resume_text:
        raise ValueError("Resume text is empty.")

    if not job_description:
        raise ValueError("Job description is empty.")

    # =========================================================
    # 1. MATCHING
    # =========================================================

    matching_result = analyze_resume_job_match(
        resume_text=resume_text,
        jd_text=job_description
    )

    # =========================================================
    # 2. EDUCATION
    # =========================================================

    education = extract_education(resume_text)

    if education:
        education_alignment = "; ".join(education)
    else:
        education_alignment = (
            "No education information was identified "
            "in the resume."
        )

    # =========================================================
    # 3. EXPERIENCE
    # =========================================================
    # IMPORTANT:
    # This comes ONLY from the resume itself.
    #
    # It does NOT come from:
    # - FAISS
    # - RAG
    # - Qwen
    # - Projects
    # - Skills
    # - Certifications
    # - Education

    experience_evidence = extract_experience_evidence(
        resume_text
    )

    # =========================================================
    # 4. BUILD FAISS INDEX
    # =========================================================

    retriever = ResumeRetriever()

    number_of_chunks = retriever.build_index(
        resume_text=resume_text,
        chunk_size=chunk_size
    )

    # =========================================================
    # 5. RETRIEVE RELEVANT RESUME EVIDENCE
    # =========================================================

    retrieval_result = retriever.retrieve_with_context(
        jd_text=job_description,
        top_k=top_k
    )

    retrieved_chunks = retrieval_result["results"]

    retrieved_context = retrieval_result["retrieved_context"]

    # =========================================================
    # 6. RAG / LLM ANALYSIS
    # =========================================================
    #
    # RAG can analyze the retrieved information.
    #
    # BUT its experience output is deliberately ignored.
    #
    # Experience is controlled by the deterministic extractor.

    rag_result = run_rag_analysis(
        resume_context=retrieved_context,
        job_description=job_description,
        matching_skills=matching_result["matching_skills"],
        missing_skills=matching_result["missing_skills"]
    )

    # We still run RAG because the pipeline uses it for
    # AI analysis, but we do not use its experience field.
    rag_data = rag_result.model_dump()

    # Prevent unused-variable confusion.
    _ = rag_data

    # =========================================================
    # 7. RECOMMENDATIONS
    # =========================================================

    recommendations = generate_recommendations(
        matching_result["missing_skills"]
    )

    # =========================================================
    # 8. FINAL RESULT
    # =========================================================

    final_result = {

        # -----------------------------------------------------
        # Overall match
        # -----------------------------------------------------

        "overall_match": matching_result["hybrid_score"],

        "match_category": matching_result[
            "match_category"
        ],

        # -----------------------------------------------------
        # Component scores
        # -----------------------------------------------------

        "tfidf_score": matching_result[
            "tfidf_score"
        ],

        "semantic_score": matching_result[
            "semantic_score"
        ],

        "skill_score": matching_result[
            "skill_score"
        ],

        # -----------------------------------------------------
        # Skills
        # -----------------------------------------------------

        "resume_skills": matching_result[
            "resume_skills"
        ],

        "jd_skills": matching_result[
            "jd_skills"
        ],

        "matching_skills": matching_result[
            "matching_skills"
        ],

        "missing_skills": matching_result[
            "missing_skills"
        ],

        # -----------------------------------------------------
        # EXPERIENCE
        # -----------------------------------------------------
        # This is the deterministic resume-based result.

        "relevant_experience": experience_evidence,

        # -----------------------------------------------------
        # EDUCATION
        # -----------------------------------------------------

        "education_alignment": education_alignment,

        # -----------------------------------------------------
        # RECOMMENDATIONS
        # -----------------------------------------------------

        "recommendations": recommendations,

        # -----------------------------------------------------
        # RETRIEVAL
        # -----------------------------------------------------

        "retrieved_chunks": retrieved_chunks,

        "retrieved_context": retrieved_context,

        "num_resume_chunks": number_of_chunks
    }

    return final_result


def analyze_resume_file(
    file_path,
    job_description,
    top_k=3,
    chunk_size=500
):
    """
    Analyze a PDF or DOCX resume directly.
    """

    # =========================================================
    # 1. EXTRACT RESUME TEXT
    # =========================================================

    resume_text = extract_resume_text(
        file_path
    )

    # =========================================================
    # 2. RUN COMPLETE PIPELINE
    # =========================================================

    result = analyze_full_resume_job_match(
        resume_text=resume_text,
        job_description=job_description,
        top_k=top_k,
        chunk_size=chunk_size
    )

    # =========================================================
    # 3. KEEP EXTRACTED TEXT
    # =========================================================

    result["extracted_resume_text"] = resume_text

    return result