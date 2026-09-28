import re


# ============================================================
# Skill dictionary
# ============================================================

SKILL_LIST = [

    # Programming
    "python", "java", "c", "c++", "c#", "r", "sql",
    "javascript", "typescript", "php", "ruby", "scala",
    "go", "kotlin", "swift",

    # Web
    "html", "css", "react", "react.js", "angular",
    "vue", "node.js", "express.js", "django", "flask",
    "fastapi", "spring", "spring boot",

    # Data / AI
    "data analysis", "data analytics", "data science",
    "data visualization", "statistics", "business analytics",
    "machine learning", "deep learning",
    "artificial intelligence", "generative ai",
    "natural language processing", "computer vision",
    "nlp", "cnn", "rnn", "lstm",

    # ML frameworks / tools
    "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn",
    "transformers", "bert", "llm", "rag",
    "langchain", "faiss", "opencv",

    # Databases
    "mysql", "postgresql", "mongodb", "oracle",
    "sql server", "sqlite", "nosql",

    # Big Data
    "hadoop", "spark", "pyspark", "hive", "kafka",

    # Cloud
    "aws", "azure", "google cloud", "gcp",
    "microsoft azure",

    # DevOps
    "docker", "kubernetes", "jenkins", "git",
    "github", "gitlab", "linux", "ci/cd",

    # APIs / Software
    "rest api", "restful api", "api",
    "microservices", "software development",
    "object oriented programming",
    "oop",

    # BI / Office
    "power bi", "tableau", "excel",
    "powerpoint", "microsoft office",

    # Business
    "e-commerce", "ecommerce", "digital marketing",
    "marketing", "sales", "customer service",
    "business development", "market research",
    "project management",

    # HR
    "human resources", "recruitment",
    "talent acquisition", "employee relations",
    "payroll",

    # Finance
    "accounting", "financial analysis", "finance",

    # Professional
    "communication", "leadership", "teamwork",
    "problem solving", "time management",
    "analytical skills"
]


# Sort longer skills first so multi-word skills
# are checked before shorter ones.
SKILL_LIST = sorted(
    set(SKILL_LIST),
    key=len,
    reverse=True
)


def normalize_text(text):
    """
    Normalize text before skill extraction.
    """
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text):
    """
    Extract explicitly mentioned skills from text.

    Returns:
        list[str]: unique skills found in the text.
    """

    text = normalize_text(text)

    found_skills = []

    for skill in SKILL_LIST:

        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_text, jd_text):
    """
    Compare skills explicitly found in a resume and job description.

    Returns:
        dict containing:
        - resume_skills
        - jd_skills
        - matching_skills
        - missing_skills
        - skill_score
    """

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    resume_skill_set = set(resume_skills)
    jd_skill_set = set(jd_skills)

    matching_skills = sorted(
        resume_skill_set.intersection(jd_skill_set)
    )

    missing_skills = sorted(
        jd_skill_set.difference(resume_skill_set)
    )

    if len(jd_skills) > 0:
        skill_score = len(matching_skills) / len(jd_skills)
    else:
        skill_score = None

    return {
        "resume_skills": sorted(resume_skill_set),
        "jd_skills": sorted(jd_skill_set),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_score": skill_score
    }