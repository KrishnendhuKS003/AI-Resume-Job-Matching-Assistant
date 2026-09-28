from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import numpy as np


# Load the same model used in the project
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def calculate_semantic_score(resume_text, jd_text):
    """
    Calculate semantic similarity between
    one resume and one job description.

    Returns:
        float: semantic similarity score from 0 to 100.
    """

    resume_text = str(resume_text).strip()
    jd_text = str(jd_text).strip()

    if not resume_text or not jd_text:
        return 0.0

    # Generate embeddings
    resume_embedding = model.encode(
        [resume_text],
        convert_to_numpy=True
    )

    jd_embedding = model.encode(
        [jd_text],
        convert_to_numpy=True
    )

    # Normalize embeddings
    resume_embedding = normalize(resume_embedding)
    jd_embedding = normalize(jd_embedding)

    # Cosine similarity using normalized dot product
    similarity = np.sum(
        resume_embedding * jd_embedding,
        axis=1
    )[0]

    # Convert to 0–100 scale
    score = similarity * 100

    return float(score)