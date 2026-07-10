import os
from dotenv import load_dotenv

load_dotenv()

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
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

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