from slack_bolt import App
from backend.services.incident_service import update_incident_status, get_incident
from backend.services.slack_service import update_incident_announcement

def register_actions(app: App):
    @app.action("acknowledge_incident")
    def handle_acknowledge(ack, body, client):
        ack()
        try:
            incident_id = int(body["actions"][0]["value"])
            user_id = body["user"]["id"]
            
            # Update incident status in the database
            incident = update_incident_status(incident_id, "acknowledged")
            if incident:
                # Update the announcement message in Slack
                update_incident_announcement(incident, user_id, "acknowledged")
        except Exception as e:
            app.logger.error(f"Error acknowledging incident: {e}")

    @app.action("resolve_incident")
    def handle_resolve(ack, body, client):
        ack()
        try:
            incident_id = int(body["actions"][0]["value"])
            user_id = body["user"]["id"]
            
            # Update incident status in the database
            incident = update_incident_status(incident_id, "resolved")
            if incident:
                # Update the announcement message in Slack
                update_incident_announcement(incident, user_id, "resolved")
        except Exception as e:
            app.logger.error(f"Error resolving incident: {e}")
