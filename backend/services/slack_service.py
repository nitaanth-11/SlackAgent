import logging

try:
    import config
except ImportError:
    from backend import config

from slack.client import get_slack_app
from slack.blocks import build_incident_blocks, build_updated_blocks
from services.incident_service import IncidentService

logger = logging.getLogger(__name__)


class SlackService:

    @staticmethod
    def post_incident(incident: dict) -> dict:
        """Post an incident card to the configured Slack channel.
        Returns the updated incident dict with slack_channel and slack_message_ts.
        """
        app = get_slack_app()
        channel = config.DEFAULT_SLACK_CHANNEL

        if not channel:
            logger.error("DEFAULT_SLACK_CHANNEL not set.")
            return incident

        blocks = build_incident_blocks(incident)
        incident_id = incident.get("incident_id", "???")

        try:
            response = app.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=f":rotating_light: New Incident: {incident.get('title', '')}",
            )

            if response.get("ok"):
                ts = response.get("ts")
                ch = response.get("channel")

                updated = IncidentService.update_slack_meta(incident_id, ch, ts)
                logger.info(f"Incident {incident_id} posted to Slack channel {ch}.")
                return updated or incident

        except Exception as e:
            logger.error(f"Failed to post incident to Slack: {e}")

        return incident

    @staticmethod
    def update_incident_message(incident: dict) -> bool:
        """Update the existing Slack message for an incident."""
        app = get_slack_app()
        channel = incident.get("slack_channel")
        ts = incident.get("slack_message_ts")

        if not channel or not ts:
            logger.warning(f"Incident {incident.get('incident_id')} missing Slack metadata, cannot update message.")
            return False

        blocks = build_updated_blocks(incident)

        try:
            response = app.client.chat_update(
                channel=channel,
                ts=ts,
                blocks=blocks,
                text=f"Incident Update: {incident.get('title', '')}",
            )
            return response.get("ok", False)

        except Exception as e:
            logger.error(f"Failed to update Slack message: {e}")
            return False
