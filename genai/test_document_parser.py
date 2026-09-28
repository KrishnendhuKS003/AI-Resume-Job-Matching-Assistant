from genai.document_parser import extract_resume_text


# --------------------------------------------------
# CHANGE THIS PATH TO YOUR ACTUAL RESUME FILE
# --------------------------------------------------

RESUME_PATH = r"C:\Users\Me\Downloads\AI Program Intern.pdf"


# --------------------------------------------------
# EXTRACT TEXT
# --------------------------------------------------

text = extract_resume_text(
    RESUME_PATH
)


# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

print("=" * 70)
print("RESUME TEXT EXTRACTION TEST")
print("=" * 70)

print("\nExtracted characters:", len(text))

print("\n===== EXTRACTED RESUME TEXT =====\n")

print(text)