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
        """
        Post an incident card to the configured Slack channel.
        Returns the updated incident dict with slack_channel and slack_message_ts.
        """

        app = get_slack_app()

        # ==========================
        # DEBUG INFORMATION
        # ==========================
        try:
            auth = app.client.auth_test()
            logger.info("=" * 60)
            logger.info("SLACK AUTH TEST")
            logger.info(auth)
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"AUTH TEST FAILED: {e}")

        channel = config.DEFAULT_SLACK_CHANNEL

        logger.info(f"DEFAULT_SLACK_CHANNEL = {channel}")
        logger.info(f"SLACK_BOT_TOKEN starts with: {config.SLACK_BOT_TOKEN[:25]}...")

        if not channel:
            logger.error("DEFAULT_SLACK_CHANNEL not set.")
            return incident

        blocks = build_incident_blocks(incident)
        incident_id = incident.get("incident_id", "???")

        try:
            logger.info(f"Posting to Slack channel: {channel}")
            response = app.client.conversations_join(
                channel=channel
            )

            logger.info(response)

            # Check whether the bot can see the channel
            info = app.client.conversations_info(channel=channel)
            logger.info("=" * 60)
            logger.info("CHANNEL INFO")
            logger.info(info)
            logger.info("=" * 60)

            # Check whether the bot is a member
            members = app.client.conversations_members(channel=channel)
            logger.info("=" * 60)
            logger.info("CHANNEL MEMBERS")
            logger.info(members)
            logger.info("=" * 60)

            response = app.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=f":rotating_light: New Incident: {incident.get('title', '')}",
            )

            logger.info("=" * 60)
            logger.info("chat_postMessage RESPONSE")
            logger.info(response)
            logger.info("=" * 60)

            if response.get("ok"):
                ts = response.get("ts")
                ch = response.get("channel")

                updated = IncidentService.update_slack_meta(
                    incident_id,
                    ch,
                    ts,
                )

                logger.info(f"Incident {incident_id} posted to Slack channel {ch}.")
                return updated or incident

            else:
                logger.error(f"Slack returned error: {response}")

        except Exception as e:
            logger.exception("Slack API Exception")

        return incident

    @staticmethod
    def update_incident_message(incident: dict) -> bool:
        """Update the existing Slack message for an incident."""

        app = get_slack_app()

        channel = incident.get("slack_channel")
        ts = incident.get("slack_message_ts")

        if not channel or not ts:
            logger.warning(
                f"Incident {incident.get('incident_id')} missing Slack metadata, cannot update message."
            )
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