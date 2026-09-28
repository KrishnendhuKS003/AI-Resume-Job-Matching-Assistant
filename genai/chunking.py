import re


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into sentence-aware chunks.

    Args:
        text: Input text.
        chunk_size: Maximum approximate characters per chunk.
        overlap: Reserved for future overlap handling.

    Returns:
        list[str]: List of text chunks.
    """

    text = str(text).strip()

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    # Split approximately at sentence boundaries.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        proposed_length = (
            len(current_chunk)
            + len(sentence)
            + 1
        )

        if proposed_length <= chunk_size:

            current_chunk += (
                (" " if current_chunk else "")
                + sentence
            )

        else:

            if current_chunk:
                chunks.append(
                    current_chunk.strip()
                )

            current_chunk = sentence

    if current_chunk:
        chunks.append(
            current_chunk.strip()
        )

    return chunks