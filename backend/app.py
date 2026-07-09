import os
import logging
from flask import Flask
from dotenv import load_dotenv

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()

# Initialize Flask app
flask_app = Flask(__name__)

# Import and register Blueprints
from backend.api.health import health_blueprint
from backend.api.incidents import incidents_blueprint
from backend.api.webhook import webhook_blueprint

flask_app.register_blueprint(health_blueprint)
flask_app.register_blueprint(incidents_blueprint)
flask_app.register_blueprint(webhook_blueprint)

# Register Slack listeners
from backend.slack.client import get_slack_app
from backend.slack.commands import register_commands
from backend.slack.actions import register_actions
from backend.slack.events import register_events

try:
    slack_app = get_slack_app()
    register_commands(slack_app)
    register_actions(slack_app)
    register_events(slack_app)
    logger.info("Slack Bolt listeners registered successfully.")
except Exception as e:
    logger.error(f"Failed to register Slack Bolt listeners: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
