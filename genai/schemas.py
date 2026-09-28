from pydantic import BaseModel, Field
from typing import List


class RAGAnalysisResult(BaseModel):
    """
    Structured output schema for the RAG/LLM analysis.
    """

    relevant_experience: List[str] = Field(
        default_factory=list
    )

    education_alignment: str = Field(
        default="Not found in the retrieved resume information."
    )

    recommendations: List[str] = Field(
        default_factory=list
    )