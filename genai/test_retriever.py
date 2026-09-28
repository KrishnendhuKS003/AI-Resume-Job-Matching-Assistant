from genai.retriever import ResumeRetriever


resume = """
Python developer with experience in data analysis,
machine learning, pandas, numpy and SQL.

Worked on machine learning projects involving
data preprocessing and model development.

Experienced with Git and software development.

Education includes a degree in Physics.
"""


job_description = """
We are looking for a candidate with Python,
machine learning and data analysis experience.
The candidate should also understand
data preprocessing and SQL.
"""


retriever = ResumeRetriever()


number_of_chunks = retriever.build_index(
    resume,
    chunk_size=200
)


print("Number of resume chunks:", number_of_chunks)


retrieved = retriever.retrieve_with_context(
    jd_text=job_description,
    top_k=3
)


print("\n===== RETRIEVED CHUNKS =====")

for result in retrieved["results"]:

    print(f"\nRank: {result['rank']}")
    print(f"Similarity: {result['score']:.4f}")
    print("Chunk:")
    print(result["chunk"])


print("\n===== RETRIEVED LLM CONTEXT =====")

print(retrieved["retrieved_context"])