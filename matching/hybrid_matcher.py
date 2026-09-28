from .skill_extractor import compare_skills
from .tfidf_matcher import calculate_tfidf_score
from .semantic_matcher import calculate_semantic_score


def min_max_normalize(value, min_value, max_value):
    """
    Normalize a value to the 0-1 range.
    """

    if max_value == min_value:
        return 0.0

    return (value - min_value) / (max_value - min_value)


def calculate_hybrid_score(
    tfidf_score,
    semantic_score,
    skill_score
):
    """
    Combine TF-IDF, semantic, and skill scores.

    Weights:
        TF-IDF  = 30%
        Semantic = 50%
        Skills   = 20%

    Returns:
        float: hybrid score from 0 to 100.
    """

    # For a live application, the scores are already
    # expressed on a 0-100 scale.

    tfidf_normalized = tfidf_score / 100
    semantic_normalized = semantic_score / 100

    # Skill score is already 0-1.
    skill_available = skill_score is not None

    if skill_available:

        hybrid_score = (
            0.30 * tfidf_normalized
            + 0.50 * semantic_normalized
            + 0.20 * skill_score
        )

    else:

        # Redistribute the unavailable 20% skill weight
        # proportionally between TF-IDF and semantic matching.
        hybrid_score = (
            0.375 * tfidf_normalized
            + 0.625 * semantic_normalized
        )

    return float(hybrid_score * 100)


def get_match_category(score):
    """
    Convert the numerical score into a user-friendly category.
    """

    if score < 40:
        return "Low Match"

    elif score < 60:
        return "Moderate Match"

    elif score < 80:
        return "Strong Match"

    else:
        return "Very Strong Match"


def analyze_resume_job_match(resume_text, jd_text):
    """
    Complete matching pipeline for one resume and one JD.

    Returns:
        dict containing:
        - TF-IDF score
        - semantic score
        - skill information
        - hybrid score
        - match category
    """

    # --------------------------------------------------------
    # 1. TF-IDF matching
    # --------------------------------------------------------

    tfidf_score = calculate_tfidf_score(
        resume_text,
        jd_text
    )

    # --------------------------------------------------------
    # 2. Semantic matching
    # --------------------------------------------------------

    semantic_score = calculate_semantic_score(
        resume_text,
        jd_text
    )

    # --------------------------------------------------------
    # 3. Skill extraction
    # --------------------------------------------------------

    skill_result = compare_skills(
        resume_text,
        jd_text
    )

    skill_score = skill_result["skill_score"]

    # --------------------------------------------------------
    # 4. Hybrid score
    # --------------------------------------------------------

    hybrid_score = calculate_hybrid_score(
        tfidf_score,
        semantic_score,
        skill_score
    )

    # --------------------------------------------------------
    # 5. User-friendly category
    # --------------------------------------------------------

    match_category = get_match_category(
        hybrid_score
    )

    return {
        "tfidf_score": round(tfidf_score, 2),
        "semantic_score": round(semantic_score, 2),
        "skill_score": (
            round(skill_score * 100, 2)
            if skill_score is not None
            else None
        ),
        "hybrid_score": round(hybrid_score, 2),
        "match_category": match_category,
        "resume_skills": skill_result["resume_skills"],
        "jd_skills": skill_result["jd_skills"],
        "matching_skills": skill_result["matching_skills"],
        "missing_skills": skill_result["missing_skills"]
    }