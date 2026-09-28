from genai.full_pipeline import analyze_resume_file


# ============================================================
# RESUME FILE
# ============================================================

RESUME_PATH = r"C:\Users\Me\Downloads\AI Program Intern.pdf"


# ============================================================
# JOB DESCRIPTION
# ============================================================

JOB_DESCRIPTION = """
We are looking for a candidate with Python,
machine learning and data analysis experience.

The candidate should understand data preprocessing
and SQL.

TensorFlow experience is preferred.
"""


# ============================================================
# RUN FILE-BASED FULL PIPELINE
# ============================================================

print("=" * 70)
print("FILE-BASED RESUME MATCHING PIPELINE")
print("=" * 70)

print("\nResume file:")
print(RESUME_PATH)

print("\nExtracting resume and running full pipeline...")


result = analyze_resume_file(
    file_path=RESUME_PATH,
    job_description=JOB_DESCRIPTION,
    top_k=3,
    chunk_size=500
)


# ============================================================
# OVERALL MATCH
# ============================================================

print("\n" + "=" * 70)
print("OVERALL MATCH")
print("=" * 70)

print(f"Overall Match: {result['overall_match']}/100")
print(f"Match Category: {result['match_category']}")


# ============================================================
# COMPONENT SCORES
# ============================================================

print("\n" + "=" * 70)
print("COMPONENT SCORES")
print("=" * 70)

print(f"TF-IDF Score:     {result['tfidf_score']}")
print(f"Semantic Score:   {result['semantic_score']}")
print(f"Skill Match:      {result['skill_score']}")


# ============================================================
# MATCHING SKILLS
# ============================================================

print("\n" + "=" * 70)
print("MATCHING SKILLS")
print("=" * 70)

if result["matching_skills"]:
    for skill in result["matching_skills"]:
        print(f"- {skill}")
else:
    print("No matching skills found.")


# ============================================================
# MISSING SKILLS
# ============================================================

print("\n" + "=" * 70)
print("MISSING / WEAK SKILLS")
print("=" * 70)

if result["missing_skills"]:
    for skill in result["missing_skills"]:
        print(f"- {skill}")
else:
    print("No missing skills identified.")


# ============================================================
# RELEVANT EXPERIENCE
# ============================================================

print("\n" + "=" * 70)
print("RELEVANT EXPERIENCE")
print("=" * 70)

if result["relevant_experience"]:
    for experience in result["relevant_experience"]:
        print(f"- {experience}")
else:
    print("No relevant experience evidence found.")


# ============================================================
# EDUCATION
# ============================================================

print("\n" + "=" * 70)
print("EDUCATION ALIGNMENT")
print("=" * 70)

print(result["education_alignment"])


# ============================================================
# RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)

if result["recommendations"]:
    for recommendation in result["recommendations"]:
        print(f"- {recommendation}")
else:
    print("No recommendations generated.")


# ============================================================
# RETRIEVED RESUME EVIDENCE
# ============================================================

print("\n" + "=" * 70)
print("RETRIEVED RESUME EVIDENCE")
print("=" * 70)

print(f"Number of resume chunks: {result['num_resume_chunks']}")

for chunk in result["retrieved_chunks"]:

    print("\n" + "-" * 60)

    print(f"Rank: {chunk['rank']}")
    print(f"Similarity: {chunk['score']:.4f}")

    print("\nResume Chunk:")
    print(chunk["chunk"])


# ============================================================
# EXTRACTED RESUME TEXT
# ============================================================

print("\n" + "=" * 70)
print("FILE EXTRACTION")
print("=" * 70)

print(
    "Extracted characters:",
    len(result["extracted_resume_text"])
)


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("FILE-BASED PIPELINE TEST COMPLETED")
print("=" * 70)