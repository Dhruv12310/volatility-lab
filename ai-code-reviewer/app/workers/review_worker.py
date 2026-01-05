from celery import Celery
import requests
from app.config import settings
from app.github.auth import get_installation_token
from app.ai.reviewer import review_pr
from app.github.comments import post_pr_comment  # ✅ ADDED

celery = Celery(
    "review_worker",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BROKER_URL,
)


def extract_diffs(files: list[dict]) -> str:
    """
    Extract unified diff patches from GitHub PR files API response
    """
    diffs = []

    for f in files:
        patch = f.get("patch")
        if patch:
            diffs.append(
                f"FILE: {f['filename']}\n{patch}"
            )

    return "\n\n".join(diffs)


@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def process_pr_review(self, payload: dict):
    pr_number = payload["pull_request"]["number"]
    repo = payload["repository"]["full_name"]
    installation_id = payload["installation"]["id"]

    print(f"[WORKER] Reviewing PR #{pr_number} in {repo}")

    # 🔐 GitHub App auth
    token = get_installation_token(installation_id)

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    # 🔹 Fetch PR metadata
    pr_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    pr_response = requests.get(pr_url, headers=headers)
    pr_response.raise_for_status()
    pr_data = pr_response.json()

    print(f"[WORKER] PR title: {pr_data['title']}")

    # 🔹 Fetch PR files (diffs)
    files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    files_response = requests.get(files_url, headers=headers)
    files_response.raise_for_status()
    files = files_response.json()

    diff_text = extract_diffs(files)

    if not diff_text:
        print("[WORKER] No code diffs found — skipping AI review")
        return

    # 🤖 AI Code Review
    print("[WORKER] Sending diffs to AI reviewer...")
    review = review_pr(diff_text)

    print("\n===== AI CODE REVIEW =====")
    print(review)
    print("==========================")

    # 📝 Post review as PR comment ✅ ADDED
    comment_body = f"""## 🤖 AI Code Review

{review}

---
_This review was generated automatically by an AI assistant._
"""

    post_pr_comment(
        repo=repo,
        pr_number=pr_number,
        token=token,
        body=comment_body,
    )
