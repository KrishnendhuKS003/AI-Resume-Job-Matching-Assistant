from genai.recommendations import (
    generate_recommendations
)


missing_skills = [
    "tensorflow",
    "docker",
    "aws"
]


recommendations = generate_recommendations(
    missing_skills
)


print("===== RECOMMENDATIONS =====")

for recommendation in recommendations:
    print("-", recommendation)