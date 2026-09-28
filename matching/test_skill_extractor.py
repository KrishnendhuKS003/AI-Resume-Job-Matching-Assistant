from skill_extractor import compare_skills


resume = """
Python developer with experience in machine learning,
pandas, numpy, SQL, Git and data analysis.
"""


job_description = """
We are looking for a candidate with Python,
machine learning, SQL and TensorFlow experience.
"""


result = compare_skills(resume, job_description)


print("\nResume skills:")
print(result["resume_skills"])

print("\nJob description skills:")
print(result["jd_skills"])

print("\nMatching skills:")
print(result["matching_skills"])

print("\nMissing skills:")
print(result["missing_skills"])

print("\nSkill score:")
print(result["skill_score"])