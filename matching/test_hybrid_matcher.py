from matching.hybrid_matcher import analyze_resume_job_match


resume = """
Python developer with experience in machine learning,
pandas, numpy, SQL, Git and data analysis.
"""


job_description = """
We are looking for a Python developer with
machine learning, SQL and TensorFlow experience.
"""


result = analyze_resume_job_match(
    resume,
    job_description
)


print("\n===== RESUME-JD MATCH ANALYSIS =====")

print("\nTF-IDF Score:")
print(result["tfidf_score"])

print("\nSemantic Score:")
print(result["semantic_score"])

print("\nSkill Score:")
print(result["skill_score"])

print("\nHybrid Score:")
print(result["hybrid_score"])

print("\nMatch Category:")
print(result["match_category"])

print("\nResume Skills:")
print(result["resume_skills"])

print("\nJD Skills:")
print(result["jd_skills"])

print("\nMatching Skills:")
print(result["matching_skills"])

print("\nMissing Skills:")
print(result["missing_skills"])