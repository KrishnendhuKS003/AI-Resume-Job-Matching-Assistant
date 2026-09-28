from tfidf_matcher import calculate_tfidf_score


resume = """
Python developer with experience in machine learning,
pandas, numpy, SQL and data analysis.
"""


job_description = """
We are looking for a Python developer with
machine learning and SQL experience.
"""


score = calculate_tfidf_score(
    resume,
    job_description
)


print("TF-IDF Match Score:", round(score, 2))