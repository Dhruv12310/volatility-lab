import requests

def post_pr_comment(repo: str, pr_number: int, token: str, body: str):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.post(
        url,
        headers=headers,
        json={"body": body},
        timeout=10,
    )

    response.raise_for_status()
