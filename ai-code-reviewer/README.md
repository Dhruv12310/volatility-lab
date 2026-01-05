# 🤖 AI GitHub Pull Request Review Bot

An AI-powered GitHub App that automatically reviews pull requests, analyzes code diffs, and posts structured feedback directly on the PR — just like a human reviewer.

---

## 🚀 What It Does

When a Pull Request is opened or updated:

1. GitHub sends a webhook event
2. A FastAPI server securely receives and verifies the request
3. A Celery worker processes the PR asynchronously
4. The bot fetches PR metadata and code diffs
5. An AI model reviews the code changes
6. The bot posts a detailed review comment on the PR

All of this happens automatically with no manual intervention.

---

## 🧠 Key Features

- GitHub App–based authentication (secure & production-grade)
- Webhook signature verification
- Asynchronous background processing using Celery + Redis
- Unified diff extraction from PR files
- AI-generated code reviews covering:
  - Bugs
  - Code Quality
  - Security
  - Performance
- Automatic PR comments by a GitHub bot account
- Retry logic and fault tolerance for external API failures

---

## 🏗 Architecture Overview

```
GitHub Pull Request Event
        ↓
GitHub Webhook
        ↓
FastAPI Server
        ↓
Signature Verification
        ↓
Celery Task Queue (Redis)
        ↓
GitHub App Authentication (JWT → Installation Token)
        ↓
Fetch PR Metadata & Diffs
        ↓
AI Code Review
        ↓
Post Review Comment on Pull Request
```

---

## 📸 Example Output

The bot automatically posts a structured AI-generated review directly on the pull request, including:

- Bug analysis
- Code quality feedback
- Security considerations
- Performance insights
- Actionable recommendations

(See screenshots in the repository for real PR examples.)

---

## 🛠 Tech Stack

- Python 3.11+
- FastAPI
- Celery
- Redis
- GitHub Apps API
- OpenAI API
- ngrok (development)

---

## ⚙️ Local Setup (Development Mode)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Dhruv12310/Github-pr-review-bot.git
cd Github-pr-review-bot
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_WEBHOOK_SECRET=dev
REDIS_BROKER_URL=redis://localhost:6379/0

GITHUB_APP_ID=your_github_app_id
GITHUB_PRIVATE_KEY_PATH=path/to/private-key.pem

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
```

> Never commit `.env` or private keys.

---

### 5️⃣ Start Redis

```bash
redis-server
```

### 6️⃣ Start FastAPI Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 7️⃣ Start Celery Worker

```bash
celery -A app.workers.review_worker worker --loglevel=info --pool=solo
```

---

## 🌐 Webhook Setup (Local Dev)

Expose the local server using ngrok:

```bash
ngrok http 8000
```

Set the GitHub App webhook URL to:

```
https://<your-ngrok-id>.ngrok-free.dev/webhooks/github
```

---

## 📈 Why This Project Matters

This project demonstrates real-world, production-grade system design:

- Event-driven architecture
- Secure GitHub App authentication
- Asynchronous background processing
- AI integration in developer workflows
- Scalable and extensible design

This is the same class of architecture used by professional developer tools and SaaS platforms.

---

## 🧑‍💻 Author

Dhruv Bhatt  
GitHub: https://github.com/Dhruv12310

---

## 📜 License

MIT License
