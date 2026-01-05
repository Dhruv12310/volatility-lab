from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a senior software engineer reviewing a GitHub pull request.
Give clear, concise, actionable feedback.
Focus on:
- Bugs
- Code quality
- Security
- Performance
"""

def review_pr(diff_text: str) -> str:
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Review the following git diff:\n\n{diff_text}",
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
