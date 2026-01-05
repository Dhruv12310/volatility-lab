from fastapi import APIRouter, Request, Header, HTTPException
from app.utils.security import verify_github_signature
from app.workers.review_worker import process_pr_review

router = APIRouter()

@router.post("/webhooks/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(None),
    x_github_event: str | None = Header(None),
):
    body = await request.body()

    if not verify_github_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid GitHub signature")

    payload = await request.json()

    if x_github_event == "pull_request":
        action = payload.get("action")
        if action in {"opened", "synchronize"}:
            process_pr_review.delay(payload)

    return {"status": "accepted"}
