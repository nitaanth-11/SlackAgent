import os
from dotenv import load_dotenv

# Find and load .env file from the current directory or parent directories
base_dir = os.path.abspath(os.path.dirname(__file__))
# Check if .env exists in backend/ or root SlackAgent/
backend_env = os.path.join(base_dir, ".env")
root_env = os.path.join(os.path.dirname(base_dir), ".env")

if os.path.exists(backend_env):
    load_dotenv(backend_env)
elif os.path.exists(root_env):
    load_dotenv(root_env)
else:
    load_dotenv()  # Fallback to standard environment search

# Slack configurations
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET") or os.getenv("SLACK_SIGNINIG_SECRET")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
DEFAULT_SLACK_CHANNEL = os.getenv("DEFAULT_SLACK_CHANNEL", "C0123456789")

# Supabase configurations
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE") or os.getenv("SUPABASE_ANON") or os.getenv("SUPABASE_API") or os.getenv("SUPABASE_KEY")
DATABASE_URL = os.getenv("DATABASE-URL") or os.getenv("DATABASE_URL")

# Flask server configuration
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "true").lower() in ("true", "1", "yes")

# Validate configuration presence and log/warn appropriately
def validate_config():
    missing = []
    if not SLACK_BOT_TOKEN:
        missing.append("SLACK_BOT_TOKEN")
    if not SLACK_SIGNING_SECRET:
        missing.append("SLACK_SIGNING_SECRET")
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing.append("SUPABASE_KEY")
    return missing
