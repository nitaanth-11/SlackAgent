import logging
from slack_bolt import App
from ai.services.offline_detector import offline_detector
from ai.services.offline_queue import offline_queue


logger = logging.getLogger(__name__)

def register_commands(app: App):

    @app.command("/incident")
    def handle_incident_command(ack, body, client):
        """Open the incident creation modal from Slack."""
        ack()
        trigger_id = body["trigger_id"]

        try:
            client.views_open(
                trigger_id=trigger_id,
                view={
                    "type": "modal",
                    "callback_id": "create_incident_modal",
                    "title": {"type": "plain_text", "text": "Report Incident"},
                    "submit": {"type": "plain_text", "text": "Create"},
                    "close": {"type": "plain_text", "text": "Cancel"},
                    "blocks": [
                        {
                            "type": "input",
                            "block_id": "title_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "title_input",
                                "placeholder": {"type": "plain_text", "text": "Brief title"},
                            },
                            "label": {"type": "plain_text", "text": "Title"},
                        },
                        {
                            "type": "input",
                            "block_id": "description_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "description_input",
                                "multiline": True,
                                "placeholder": {"type": "plain_text", "text": "What happened?"},
                            },
                            "label": {"type": "plain_text", "text": "Description"},
                        },
                        {
                            "type": "input",
                            "block_id": "service_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "service_input",
                                "placeholder": {"type": "plain_text", "text": "e.g. payments-api"},
                            },
                            "label": {"type": "plain_text", "text": "Service"},
                        },
                        {
                            "type": "input",
                            "block_id": "severity_block",
                            "element": {
                                "type": "static_select",
                                "action_id": "severity_select",
                                "placeholder": {"type": "plain_text", "text": "Select severity"},
                                "options": [
                                    {"text": {"type": "plain_text", "text": ":large_blue_circle: Low"}, "value": "LOW"},
                                    {"text": {"type": "plain_text", "text": ":large_yellow_circle: Medium"}, "value": "MEDIUM"},
                                    {"text": {"type": "plain_text", "text": ":large_orange_circle: High"}, "value": "HIGH"},
                                    {"text": {"type": "plain_text", "text": ":red_circle: Critical"}, "value": "CRITICAL"},
                                ],
                            },
                            "label": {"type": "plain_text", "text": "Severity"},
                        },
                    ],
                },
            )
        except Exception as e:
            logger.error(f"Failed to open incident modal: {e}")
            try:
                client.chat_postEphemeral(
                    channel=body["channel_id"],
                    user=body["user_id"],
                    text="⚠️ Failed to open the form. Please try again.",
                )
            except Exception:
                pass

    @app.view("create_incident_modal")
    def handle_modal_submission(ack, body, client, view):
        """Handle the incident creation modal submission."""
        values = view["state"]["values"]

        title = (values["title_block"]["title_input"]["value"] or "").strip()
        description = (values["description_block"]["description_input"]["value"] or "").strip()
        service = (values["service_block"]["service_input"]["value"] or "").strip()
        severity_opt = values["severity_block"]["severity_select"].get("selected_option")

        errors = {}
        if not title:
            errors["title_block"] = "Title is required."
        if not description:
            errors["description_block"] = "Description is required."
        if not service:
            errors["service_block"] = "Service is required."
        if not severity_opt:
            errors["severity_block"] = "Please select a severity level."

        if errors:
            ack(response_action="errors", errors=errors)
            return

        ack()

        data = {
            "title": title,
            "description": description,
            "service": service,
            "severity": severity_opt["value"],
        }

        from services.incident_service import IncidentService
        from services.slack_service import SlackService

        try:
            online = offline_detector.check_connection()

            if online:
                incident = IncidentService.create_incident(data)
                SlackService.post_incident(incident)
            else:
                offline_queue.add_incident(data)
        except Exception as e:
            logger.error(f"Failed to create incident: {e}")
            try:
                client.chat_postMessage(
                    channel=body["user"]["id"],
                    text="⚠️ Failed to create incident. Please try again.",
                )
            except Exception:
                pass
