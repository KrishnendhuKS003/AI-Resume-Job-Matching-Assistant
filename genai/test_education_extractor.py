from genai.education_extractor import extract_education


resume = """
Python developer with experience in machine learning.

Education includes a degree in Physics.
"""


education = extract_education(resume)


print("===== EDUCATION EXTRACTION =====")
print(education)