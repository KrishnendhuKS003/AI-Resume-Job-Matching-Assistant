from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import faiss

from .chunking import chunk_text


MODEL_NAME = "all-MiniLM-L6-v2"


class ResumeRetriever:
    """
    Creates embeddings for resume chunks and retrieves
    the chunks most relevant to a job description.
    """

    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, resume_text, chunk_size=500):
        """
        Split the resume into chunks, create embeddings,
        and build a FAISS similarity index.

        Returns:
            int: Number of chunks created.
        """

        self.chunks = chunk_text(
            resume_text,
            chunk_size=chunk_size
        )

        if not self.chunks:
            raise ValueError("No resume text available.")

        embeddings = self.model.encode(
            self.chunks,
            convert_to_numpy=True
        )

        embeddings = normalize(
            embeddings
        ).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

        return len(self.chunks)

    def retrieve(self, jd_text, top_k=3):
        """
        Retrieve the most relevant resume chunks
        for the given job description.

        Returns:
            list[dict]: Retrieved chunks with rank,
            similarity score and text.
        """

        if self.index is None:
            raise ValueError(
                "FAISS index has not been built yet."
            )

        if not jd_text or not str(jd_text).strip():
            raise ValueError(
                "Job description is empty."
            )

        # Create embedding for the job description.
        jd_embedding = self.model.encode(
            [str(jd_text).strip()],
            convert_to_numpy=True
        )

        # Normalize so inner product = cosine similarity.
        jd_embedding = normalize(
            jd_embedding
        ).astype("float32")

        # Never request more chunks than actually exist.
        k = min(
            top_k,
            len(self.chunks)
        )

        scores, indices = self.index.search(
            jd_embedding,
            k
        )

        results = []

        for rank, (score, index) in enumerate(
            zip(scores[0], indices[0]),
            start=1
        ):

            results.append({
                "rank": rank,
                "score": float(score),
                "chunk": self.chunks[index]
            })

        return results

    def build_retrieved_context(self, results):
        """
        Convert retrieved chunks into a structured
        evidence context for the LLM.
        """

        if not results:
            return (
                "No relevant resume evidence was retrieved."
            )

        context_parts = []

        for result in results:

            rank = result["rank"]
            score = result["score"]
            chunk = result["chunk"]

            context_parts.append(
                f"[Resume Evidence {rank} | "
                f"similarity: {score:.4f}]\n"
                f"{chunk}"
            )

        return "\n\n".join(context_parts)

    def retrieve_with_context(
        self,
        jd_text,
        top_k=3
    ):
        """
        Retrieve relevant resume chunks and also
        create a formatted context for the LLM.

        Returns:
            dict containing:
            - results
            - retrieved_context
        """

        results = self.retrieve(
            jd_text=jd_text,
            top_k=top_k
        )

        retrieved_context = self.build_retrieved_context(
            results
        )

        return {
            "results": results,
            "retrieved_context": retrieved_context
        }