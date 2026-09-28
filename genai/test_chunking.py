from chunking import chunk_text


text = """
Python is a programming language widely used for data analysis.
Machine learning allows systems to learn patterns from data.
Natural language processing is used to work with human language.
Generative AI can produce text, summaries and recommendations.
"""


chunks = chunk_text(
    text,
    chunk_size=150
)


print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):

    print(f"\nChunk {i}:")
    print(chunk)