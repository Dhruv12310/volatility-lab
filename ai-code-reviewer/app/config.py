from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    # Webhook / Infra
    GITHUB_WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    REDIS_BROKER_URL: str = os.getenv("REDIS_BROKER_URL", "")

    # GitHub App
    GITHUB_APP_ID: str = os.getenv("GITHUB_APP_ID", "")
    GITHUB_PRIVATE_KEY_PATH: str = os.getenv("GITHUB_PRIVATE_KEY_PATH", "")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


settings = Settings()
