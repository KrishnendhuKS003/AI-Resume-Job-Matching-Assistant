import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_text(text):
    """
    Basic text normalization for TF-IDF matching.
    """

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_tfidf_score(resume_text, jd_text):
    """
    Calculate TF-IDF cosine similarity between
    one resume and one job description.

    Returns:
        float: similarity score from 0 to 100.
    """

    resume_text = normalize_text(resume_text)
    jd_text = normalize_text(jd_text)

    documents = [resume_text, jd_text]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    score = similarity * 100

    return float(score)