import jwt
import time
import requests
from pathlib import Path
from app.config import settings


def _load_private_key() -> str:
    key_path = Path(settings.GITHUB_PRIVATE_KEY_PATH)
    return key_path.read_text()


def generate_app_jwt() -> str:
    """
    Generates a short-lived JWT for GitHub App authentication.
    """
    now = int(time.time())

    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60),
        "iss": settings.GITHUB_APP_ID,
    }

    private_key = _load_private_key()

    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_token(installation_id: int) -> str:
    """
    Exchanges App JWT for an installation access token.
    """
    jwt_token = generate_app_jwt()

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    return response.json()["token"]
