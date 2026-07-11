import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
# -------------------------
# Slack
# -------------------------

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

DEFAULT_SLACK_CHANNEL = os.getenv("DEFAULT_SLACK_CHANNEL")

# -------------------------
# Supabase
# -------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SERVICE_KEY")
print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY exists:", bool(SUPABASE_SECRET_KEY))
# -------------------------
# Database
# -------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------------
# FastAPI
# -------------------------

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
ENV = os.getenv("ENV", "development")


def validate_config():
    required = {
        "SLACK_BOT_TOKEN": SLACK_BOT_TOKEN,
        "SLACK_SIGNING_SECRET": SLACK_SIGNING_SECRET,
        "SUPABASE_URL": SUPABASE_URL,
    }

    missing = [key for key, value in required.items() if not value]

    return missing