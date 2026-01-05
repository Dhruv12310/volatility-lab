from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def review_pr(diff_text: str) -> str:
    prompt = f"""
You are a senior software engineer performing a GitHub Pull Request review.

Review the following code diff and provide:
- Potential bugs
- Code quality issues
- Security concerns
- Suggestions for improvement

Be concise and technical.

CODE DIFF:
{diff_text}
"""

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a professional code reviewer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
