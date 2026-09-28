import re


EDUCATION_PATTERNS = [
    r"\b(?:b\.?sc|bachelor(?:'s)?|bachelors)\b[^.\n]*",
    r"\b(?:b\.?tech|b\.?e|bachelor of technology)\b[^.\n]*",
    r"\b(?:m\.?sc|master(?:'s)?|masters)\b[^.\n]*",
    r"\b(?:m\.?tech|m\.?e|master of technology)\b[^.\n]*",
    r"\b(?:ph\.?d|doctorate)\b[^.\n]*",
    r"\b(?:degree|graduation|graduate)\b[^.\n]*",
]


def extract_education(text):
    """
    Extract explicitly mentioned education information.

    Returns:
        list[str]
    """

    text = str(text).strip()

    if not text:
        return []

    education = []

    for pattern in EDUCATION_PATTERNS:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            cleaned = re.sub(
                r"\s+",
                " ",
                match
            ).strip()

            if cleaned and cleaned not in education:
                education.append(cleaned)

    return education