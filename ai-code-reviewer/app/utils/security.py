import hmac
import hashlib
from app.config import settings


def verify_github_signature(payload: bytes, signature: str | None) -> bool:
    """
    Verifies GitHub webhook signature using HMAC SHA256.

    Local development bypass:
    - Set GITHUB_WEBHOOK_SECRET=dev
    """

    # 🔹 Explicit local development bypass
    if settings.GITHUB_WEBHOOK_SECRET == "dev":
        return True

    # 🔹 Signature must exist
    if not signature:
        return False

    # 🔹 Signature format: sha256=<hash>
    try:
        sha_name, signature_hash = signature.split("=", 1)
    except ValueError:
        return False

    if sha_name != "sha256":
        return False

    # 🔹 Compute HMAC using webhook secret
    mac = hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    )

    # 🔹 Constant-time comparison (prevents timing attacks)
    return hmac.compare_digest(mac.hexdigest(), signature_hash)
