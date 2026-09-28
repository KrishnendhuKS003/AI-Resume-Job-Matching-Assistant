import re


# ============================================================
# EXPERIENCE SECTION HEADINGS
# ============================================================

EXPERIENCE_HEADINGS = {
    "experience",
    "work experience",
    "professional experience",
    "work history",
    "employment history",
    "employment",
    "internship experience",
    "internship experiences",
}


# ============================================================
# OTHER SECTION HEADINGS
# ============================================================

OTHER_SECTION_HEADINGS = {
    "professional summary",
    "summary",
    "profile",
    "career objective",
    "objective",

    "technical skills",
    "technical skill",
    "skills",
    "key skills",
    "core skills",

    "education",
    "academic background",
    "academic qualifications",

    "projects",
    "project",
    "academic projects",
    "personal projects",

    "certifications",
    "certification",
    "courses",

    "additional information",
    "additional skills",
    "soft skills",
    "languages",
    "interests",

    "achievements",
    "awards",
    "publications",
    "references",

    "availability",
}


# ============================================================
# EXPLICIT FRESHER / ENTRY-LEVEL WORDS
# ============================================================

FRESHER_PATTERNS = [
    r"\bfresher\b",
    r"\bfresh graduate\b",
    r"\brecent graduate\b",
    r"\bnew graduate\b",
    r"\bentry[- ]level\b",
    r"\bseeking internship\b",
    r"\bseeking an internship\b",
    r"\blooking for internship\b",
    r"\blooking for an internship\b",
    r"\bopen to internship\b",
    r"\bopen to internships\b",
    r"\bstudent seeking\b",
    r"\bgraduate seeking\b",
]


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_line(line):
    """
    Clean a line while preserving its actual content.
    """

    line = str(line)

    line = line.replace("\xa0", " ")

    line = re.sub(
        r"[ \t]+",
        " ",
        line
    )

    return line.strip()


# ============================================================
# NORMALIZE POSSIBLE HEADING
# ============================================================

def normalize_heading(line):
    """
    Normalize a line ONLY for heading comparison.
    """

    line = clean_line(line)

    # Remove bullets
    line = re.sub(
        r"^[•●▪■\-–—]+\s*",
        "",
        line
    )

    # Remove trailing punctuation
    line = re.sub(
        r"[:|]+$",
        "",
        line
    )

    return line.strip().lower()


# ============================================================
# CHECK IF LINE IS A STANDALONE HEADING
# ============================================================

def is_standalone_heading(line, heading_set):
    """
    A section heading must be the entire line.

    For example:

        EXPERIENCE
        Work Experience
        PROFESSIONAL EXPERIENCE

    are valid.

    But:

        Experienced in Python and SQL

    is NOT a heading.
    """

    normalized = normalize_heading(line)

    return normalized in heading_set


# ============================================================
# SPLIT RESUME INTO LINES
# ============================================================

def get_resume_lines(text):
    """
    Preserve the PDF-extracted line structure.
    """

    text = str(text)

    raw_lines = text.splitlines()

    lines = []

    for line in raw_lines:

        cleaned = clean_line(line)

        if cleaned:
            lines.append(cleaned)

    return lines


# ============================================================
# EXTRACT ACTUAL EXPERIENCE SECTION
# ============================================================

def extract_experience_section(text):
    """
    Extract ONLY the content between a standalone Experience
    heading and the next standalone major section heading.
    """

    lines = get_resume_lines(text)

    if not lines:
        return []

    start_index = None

    # --------------------------------------------------------
    # Find standalone Experience heading
    # --------------------------------------------------------

    for index, line in enumerate(lines):

        if is_standalone_heading(
            line,
            EXPERIENCE_HEADINGS
        ):
            start_index = index
            break

    # No Experience section
    if start_index is None:
        return []

    # --------------------------------------------------------
    # Collect content until next major section
    # --------------------------------------------------------

    experience_lines = []

    for line in lines[start_index + 1:]:

        # Stop at another major section
        if is_standalone_heading(
            line,
            OTHER_SECTION_HEADINGS
        ):
            break

        # Stop if another experience heading appears
        if is_standalone_heading(
            line,
            EXPERIENCE_HEADINGS
        ):
            continue

        experience_lines.append(line)

    # Remove empty results
    experience_lines = [
        line
        for line in experience_lines
        if line.strip()
    ]

    return experience_lines


# ============================================================
# FIND EXPLICIT FRESHER / INTERN STATEMENT
# ============================================================

def find_explicit_candidate_status(text):
    """
    Search the resume for an explicit statement such as:

    Fresher
    Recent graduate
    Entry-level
    Seeking internship

    We return the actual line from the resume.
    """

    lines = get_resume_lines(text)

    for line in lines:

        lower_line = line.lower()

        for pattern in FRESHER_PATTERNS:

            if re.search(
                pattern,
                lower_line
            ):
                return [line]

    return []


# ============================================================
# MAIN FUNCTION
# ============================================================

def extract_experience_evidence(text):
    """
    Determine what should appear in the Experience section.

    Priority:

    1. Actual Experience section
    2. Explicit fresher/intern/entry-level statement
    3. "No prior experience mentioned."

    Nothing is inferred from projects, skills, education,
    certifications, or RAG results.
    """

    # --------------------------------------------------------
    # STEP 1: Actual Experience section
    # --------------------------------------------------------

    experience = extract_experience_section(text)

    if experience:
        return experience

    # --------------------------------------------------------
    # STEP 2: Explicit candidate status
    # --------------------------------------------------------

    candidate_status = find_explicit_candidate_status(text)

    if candidate_status:
        return candidate_status

    # --------------------------------------------------------
    # STEP 3: No experience information
    # --------------------------------------------------------

    return [
        "No prior experience mentioned."
    ]