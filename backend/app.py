import os
import sys

# Enable importing both 'backend.xxx' and local modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slack_bolt.adapter.fastapi import SlackRequestHandler
import logging

import config

# API Routers
from api.health import router as health_router
from api.incidents import router as incidents_router
from api.webhook import router as webhook_router

# Slack
from slack.client import get_slack_app
from slack.commands import register_commands
from slack.actions import register_actions
from slack.events import register_events
from ai.services.offline_detector import offline_detector
from ai.services.offline_queue import offline_queue
from ai.services.sync_service import sync_service
from ai.services.location_cache import location_cache
from ai.services.sms.mock_sms import sms_provider
from ai.services.contact_cache import contact_cache
import threading
import time

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Validate Environment Variables
# --------------------------------------------------

missing = config.validate_config()

if missing:
    logger.warning(f"Missing environment variables: {', '.join(missing)}")

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="OpsPilot Incident Backend",
    version="1.0.0",
    description="Slack Native Incident Intelligence Backend",
)

# --------------------------------------------------
# Register API Routers
# --------------------------------------------------

app.include_router(health_router)
app.include_router(incidents_router)
app.include_router(webhook_router)

# --------------------------------------------------
# Slack Bolt Initialization
# --------------------------------------------------

slack_handler = None

try:
    slack_app = get_slack_app()

    register_commands(slack_app)
    register_actions(slack_app)
    register_events(slack_app)

    slack_handler = SlackRequestHandler(slack_app)

    logger.info("Slack Bolt initialized successfully.")

except Exception as e:
    logger.exception(f"Failed to initialize Slack Bolt: {e}")

# --------------------------------------------------
# Background Network Monitor
# --------------------------------------------------

def monitor_network():
    while True:
        online = offline_detector.check_connection()

        if online != offline_detector.previous_status:

            if online:
                logger.info("Internet connection restored!")
                sync_service.sync()
            else:
                logger.warning("Internet connection lost!")

                offline_queue.add_incident({
                    "id": f"OFFLINE-{int(time.time())}",
                    "severity": "UNKNOWN",
                    "summary": "Internet connectivity lost",
                    "location": location_cache.get(),
                })

                logger.info("Incident stored in offline queue.")

                contacts = contact_cache.get_contacts()

                if contacts:
                    sms_provider.send_sms(
                        phone=contacts[0]["phone"],
                        message="⚠️ Internet lost. Incident stored locally and will sync automatically."
                    )
                else:
                    logger.warning("No emergency contact found.")         

            offline_detector.previous_status = online

        time.sleep(5)

# --------------------------------------------------
# Slack Events Endpoint
# --------------------------------------------------

@app.post("/slack/events")
async def slack_events(request: Request):
    if slack_handler is None:
        return JSONResponse(
            status_code=500,
            content={"error": "Slack handler not initialized"},
        )
    return await slack_handler.handle(request)

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "OpsPilot Backend",
        "version": "1.0.0",
    }

# --------------------------------------------------
# Network Status
# --------------------------------------------------

@app.get("/network/status")
def network_status():
    offline_detector.check_connection()
    return offline_detector.get_status()

# --------------------------------------------------
# Local Development
# --------------------------------------------------

if __name__ == "__main__":
    threading.Thread(
        target=monitor_network,
        daemon=True,
    ).start()

    import uvicorn

    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        reload=False,
    )