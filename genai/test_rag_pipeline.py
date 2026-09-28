from genai.retriever import ResumeRetriever
from genai.rag_pipeline import run_rag_analysis


# --------------------------------------------------
# 1. SAMPLE RESUME
# --------------------------------------------------

resume = """
Python developer with experience in data analysis,
machine learning, pandas, numpy and SQL.

Worked on machine learning projects involving
data preprocessing and model development.

Experienced with Git and software development.

Education includes a degree in Physics.
"""


# --------------------------------------------------
# 2. SAMPLE JOB DESCRIPTION
# --------------------------------------------------

job_description = """
We are looking for a candidate with Python,
machine learning and data analysis experience.

The candidate should also understand
data preprocessing and SQL.

TensorFlow experience is preferred.
"""


# --------------------------------------------------
# 3. DETERMINISTIC SKILL MATCHING
# --------------------------------------------------

matching_skills = [
    "machine learning",
    "python",
    "sql"
]

missing_skills = [
    "tensorflow"
]


# --------------------------------------------------
# 4. BUILD FAISS RETRIEVER
# --------------------------------------------------

retriever = ResumeRetriever()


number_of_chunks = retriever.build_index(
    resume,
    chunk_size=200
)

print("\n===== RETRIEVAL SETUP =====")
print("Resume chunks:", number_of_chunks)


# --------------------------------------------------
# 5. RETRIEVE RELEVANT RESUME EVIDENCE
# --------------------------------------------------

retrieved = retriever.retrieve_with_context(
    jd_text=job_description,
    top_k=3
)


print("\n===== RETRIEVED RESUME EVIDENCE =====")

for result in retrieved["results"]:

    print(f"\nRank: {result['rank']}")
    print(f"Similarity: {result['score']:.4f}")
    print("Chunk:")
    print(result["chunk"])


# --------------------------------------------------
# 6. GET FORMATTED RAG CONTEXT
# --------------------------------------------------

retrieved_context = retrieved["retrieved_context"]


print("\n===== RAG CONTEXT =====")
print(retrieved_context)


# --------------------------------------------------
# 7. SEND RETRIEVED CONTEXT TO QWEN
# --------------------------------------------------

result = run_rag_analysis(
    resume_context=retrieved_context,
    job_description=job_description,
    matching_skills=matching_skills,
    missing_skills=missing_skills
)


# --------------------------------------------------
# 8. DISPLAY VALIDATED RESULT
# --------------------------------------------------

print("\n===== VALIDATED RAG ANALYSIS =====")

print(result)


# --------------------------------------------------
# 9. DISPLAY AS DICTIONARY
# --------------------------------------------------

print("\n===== AS DICTIONARY =====")

print(result.model_dump())