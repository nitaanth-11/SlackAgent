import logging
from slack_bolt import App

logger = logging.getLogger(__name__)

def _is_resolved(incident_id: str, body: dict, client) -> bool:
    from services.incident_service import IncidentService
    inc = IncidentService.get_incident(incident_id) or {}
    if inc.get("status", "").upper() == "RESOLVED":
        try: client.chat_postEphemeral(channel=body["channel"]["id"], user=body["user"]["id"], text="⚠️ This incident is already resolved.")
        except Exception: pass
        return True
    return False

def register_actions(app: App):

    # --------------------------------------------------
    # Assign Owner Button
    # --------------------------------------------------

    @app.action("assign_owner")
    def handle_assign_owner(ack, body, client):
        ack()
        try:
            incident_id = body["actions"][0]["value"]
            if _is_resolved(incident_id, body, client): return
            trigger_id = body["trigger_id"]

            # Open a modal to collect the owner name
            client.views_open(
                trigger_id=trigger_id,
                view={
                    "type": "modal",
                    "callback_id": "assign_owner_modal",
                    "private_metadata": incident_id,
                    "title": {"type": "plain_text", "text": "Assign Owner"},
                    "submit": {"type": "plain_text", "text": "Assign"},
                    "close": {"type": "plain_text", "text": "Cancel"},
                    "blocks": [
                        {
                            "type": "input",
                            "block_id": "owner_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "owner_input",
                                "placeholder": {"type": "plain_text", "text": "e.g. @john or John Doe"},
                            },
                            "label": {"type": "plain_text", "text": "Owner"},
                        },
                    ],
                },
            )
        except Exception as e:
            logger.error(f"Failed to open assign owner modal: {e}")
            try:
                client.chat_postEphemeral(
                    channel=body["channel"]["id"],
                    user=body["user"]["id"],
                    text="⚠️ Something went wrong. Please try again.",
                )
            except Exception:
                pass

    @app.view("assign_owner_modal")
    def handle_assign_owner_submit(ack, body, client, view):
        owner = (view["state"]["values"]["owner_block"]["owner_input"]["value"] or "").strip()
        if not owner:
            ack(response_action="errors", errors={"owner_block": "Owner name cannot be empty."})
            return

        ack()
        try:
            incident_id = view["private_metadata"]

            from services.incident_service import IncidentService
            from services.slack_service import SlackService

            updated = IncidentService.assign_owner(incident_id, owner)
            if updated:
                SlackService.update_incident_message(updated)
        except Exception as e:
            logger.error(f"Failed to assign owner: {e}")

    # --------------------------------------------------
    # Resolve Button
    # --------------------------------------------------

    @app.action("resolve_incident")
    def handle_resolve(ack, body, client):
        ack()
        try:
            incident_id = body["actions"][0]["value"]
            if _is_resolved(incident_id, body, client): return

            from services.incident_service import IncidentService
            from services.slack_service import SlackService

            updated = IncidentService.resolve_incident(incident_id)
            if updated:
                SlackService.update_incident_message(updated)
        except Exception as e:
            logger.error(f"Failed to resolve incident: {e}")
            try:
                client.chat_postEphemeral(
                    channel=body["channel"]["id"],
                    user=body["user"]["id"],
                    text="⚠️ Something went wrong. Please try again.",
                )
            except Exception:
                pass

    # --------------------------------------------------
    # Generate Update Button
    # --------------------------------------------------

    @app.action("generate_update")
    def handle_generate_update(ack, body, client):
        ack()
        try:
            incident_id = body["actions"][0]["value"]
            if _is_resolved(incident_id, body, client): return

            from services.incident_service import IncidentService

            incident = IncidentService.get_incident(incident_id)
            if not incident:
                return

            channel = incident.get("slack_channel")
            if not channel:
                return

            # Post a threaded status update summary
            status = incident.get("status", "OPEN")
            owner = incident.get("owner") or "Unassigned"
            severity = incident.get("severity", "UNKNOWN")
            title = incident.get("title", "")
            ts = incident.get("slack_message_ts")

            update_text = (
                f":clipboard: *Incident Status Update*\n\n"
                f"*ID:* `{incident_id}`\n"
                f"*Title:* {title}\n"
                f"*Severity:* {severity}\n"
                f"*Status:* {status}\n"
                f"*Owner:* {owner}\n"
            )

            client.chat_postMessage(
                channel=channel,
                thread_ts=ts,
                text=update_text,
            )

        except Exception as e:
            logger.error(f"Failed to generate update: {e}")
            try:
                client.chat_postEphemeral(
                    channel=body["channel"]["id"],
                    user=body["user"]["id"],
                    text="⚠️ Something went wrong. Please try again.",
                )
            except Exception:
                pass
