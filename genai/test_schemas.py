from schemas import RAGAnalysisResult


result = RAGAnalysisResult(
    relevant_experience=[
        "Worked on machine learning projects involving data preprocessing and model development."
    ],
    education_alignment="Degree in Physics.",
    recommendations=[
        "Add TensorFlow experience."
    ]
)


print("\n===== VALIDATED RAG RESULT =====")

print(result)

print("\n===== AS DICTIONARY =====")

print(result.model_dump())