from slack_bolt import App

from slack.blocks import build_incident_blocks


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
            app.logger.error(f"Error opening incident modal: {e}")

    @app.view("create_incident_modal")
    def handle_modal_submission(ack, body, client, view):
        """Handle the incident creation modal submission."""
        ack()

        values = view["state"]["values"]

        data = {
            "title": values["title_block"]["title_input"]["value"],
            "description": values["description_block"]["description_input"]["value"],
            "service": values["service_block"]["service_input"]["value"],
            "severity": values["severity_block"]["severity_select"]["selected_option"]["value"],
        }

        from services.incident_service import IncidentService
        from services.slack_service import SlackService

        incident = IncidentService.create_incident(data)
        SlackService.post_incident(incident)
