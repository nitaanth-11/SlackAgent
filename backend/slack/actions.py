from slack_bolt import App


def register_actions(app: App):

    # --------------------------------------------------
    # Assign Owner Button
    # --------------------------------------------------

    @app.action("assign_owner")
    def handle_assign_owner(ack, body, client):
        ack()
        try:
            incident_id = body["actions"][0]["value"]
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
            app.logger.error(f"Error opening assign owner modal: {e}")

    @app.view("assign_owner_modal")
    def handle_assign_owner_submit(ack, body, view):
        ack()
        try:
            incident_id = view["private_metadata"]
            owner = view["state"]["values"]["owner_block"]["owner_input"]["value"]

            from services.incident_service import IncidentService
            from services.slack_service import SlackService

            updated = IncidentService.assign_owner(incident_id, owner)
            if updated:
                SlackService.update_incident_message(updated)
        except Exception as e:
            app.logger.error(f"Error assigning owner: {e}")

    # --------------------------------------------------
    # Resolve Button
    # --------------------------------------------------

    @app.action("resolve_incident")
    def handle_resolve(ack, body, client):
        ack()
        try:
            incident_id = body["actions"][0]["value"]

            from services.incident_service import IncidentService
            from services.slack_service import SlackService

            updated = IncidentService.resolve_incident(incident_id)
            if updated:
                SlackService.update_incident_message(updated)
        except Exception as e:
            app.logger.error(f"Error resolving incident: {e}")

    # --------------------------------------------------
    # Generate Update Button
    # --------------------------------------------------

    @app.action("generate_update")
    def handle_generate_update(ack, body, client):
        ack()
        try:
            incident_id = body["actions"][0]["value"]

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
            app.logger.error(f"Error generating update: {e}")
