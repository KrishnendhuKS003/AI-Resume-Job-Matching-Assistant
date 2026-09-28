from semantic_matcher import calculate_semantic_score


resume = """
Python developer with experience in machine learning,
pandas, numpy, SQL and data analysis.
"""


job_description = """
We are looking for a Python developer with
machine learning and SQL experience.
"""


score = calculate_semantic_score(
    resume,
    job_description
)


print("Semantic Match Score:", round(score, 2))