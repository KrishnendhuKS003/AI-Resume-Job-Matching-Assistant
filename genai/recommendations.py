def generate_recommendations(missing_skills):
    """
    Generate clear, user-friendly recommendations
    from the deterministic missing-skill list.

    This function does not invent missing skills.
    """

    if not missing_skills:
        return [
            "No major missing skills were identified "
            "from the detected job requirements."
        ]

    recommendations = []

    for skill in missing_skills:

        skill = str(skill).strip()

        if not skill:
            continue

        recommendation = (
            f"Consider gaining {skill} experience "
            f"to better align with the job requirements."
        )

        recommendations.append(
            recommendation
        )

    return recommendations