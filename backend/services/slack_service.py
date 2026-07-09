import logging
from backend.slack.client import get_slack_app
from backend.models.incident import Incident
from backend.slack.blocks import get_announcement_blocks, get_resolved_blocks
from backend import config

logger = logging.getLogger(__name__)

def post_incident_announcement(incident: Incident) -> bool:
    app = get_slack_app()
    channel_id = config.DEFAULT_SLACK_CHANNEL
    if not channel_id:
        logger.error("DEFAULT_SLACK_CHANNEL not set in configuration.")
        return False
        
    try:
        blocks = get_announcement_blocks(incident)
        # Post the message to the channel
        response = app.client.chat_postMessage(
            channel=channel_id,
            blocks=blocks,
            text=f"🚨 New Incident: {incident.title}"
        )
        if response.get("ok"):
            ts = response.get("ts")
            channel = response.get("channel")
            # Update the incident metadata with channel_id and message_ts
            from backend.services.incident_service import update_incident_slack_meta
            update_incident_slack_meta(incident.id, channel, ts)
            return True
    except Exception as e:
        logger.error(f"Failed to post incident announcement: {e}")
    return False

def update_incident_announcement(incident: Incident, user_name: str, status: str) -> bool:
    app = get_slack_app()
    if not incident.channel_id or not incident.message_ts:
        logger.error(f"Incident {incident.id} is missing channel_id or message_ts.")
        return False
        
    try:
        if status == "resolved":
            blocks = get_resolved_blocks(incident, user_name)
        else:
            # Under progress, acknowledged
            blocks = get_announcement_blocks(incident, acknowledged_by=user_name)
            
        response = app.client.chat_update(
            channel=incident.channel_id,
            ts=incident.message_ts,
            blocks=blocks,
            text=f"🚨 Incident Updated: {incident.title} ({status})"
        )
        return response.get("ok", False)
    except Exception as e:
        logger.error(f"Failed to update incident announcement: {e}")
    return False
