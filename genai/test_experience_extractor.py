from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from genai.experience_extractor import extract_experience_evidence


RESUME_PATH = r"C:\Users\Me\Downloads\AI Program Intern.pdf"


print("=" * 70)
print("EXPERIENCE EXTRACTION TEST")
print("=" * 70)


# ------------------------------------------------------------
# Read the already extracted PDF text manually
# ------------------------------------------------------------
# For this isolated test, we first need the PDF text.
# PyMuPDF does not require Transformers or Torchvision.

import pymupdf


document = pymupdf.open(RESUME_PATH)

pages = []

for page in document:
    text = page.get_text()

    if text:
        pages.append(text)

document.close()


resume_text = "\n".join(pages).strip()


print("\nResume characters:")
print(len(resume_text))


# ------------------------------------------------------------
# Experience extraction
# ------------------------------------------------------------

experience = extract_experience_evidence(
    resume_text
)


print("\n" + "=" * 70)
print("EXTRACTED EXPERIENCE")
print("=" * 70)


for item in experience:
    print("•", item)


print("\n" + "=" * 70)
print("TEST COMPLETED")
print("=" * 70)