from pathlib import Path

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        str: Extracted text.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    document = pymupdf.open(file_path)

    pages = []

    for page in document:
        text = page.get_text()

        if text:
            pages.append(text)

    document.close()

    extracted_text = "\n".join(pages).strip()

    if not extracted_text:
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    return extracted_text


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        str: Extracted text.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    extracted_text = "\n".join(
        paragraphs
    ).strip()

    if not extracted_text:
        raise ValueError(
            "No text could be extracted from the DOCX."
        )

    return extracted_text


def extract_resume_text(file_path):
    """
    Automatically detect PDF or DOCX and extract
    the resume text.

    Supported formats:
        - PDF
        - DOCX
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        return extract_text_from_pdf(
            file_path
        )

    elif extension == ".docx":

        return extract_text_from_docx(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please provide a PDF or DOCX file."
        )