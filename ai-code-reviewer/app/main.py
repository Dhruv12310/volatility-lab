from fastapi import FastAPI
from app.api.webhooks import router as webhook_router
from app.config import settings

print("Loaded Redis URL:", settings.REDIS_BROKER_URL)

app = FastAPI(title="AI Code Review Assistant")

app.include_router(webhook_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}