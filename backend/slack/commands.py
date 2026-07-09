from slack_bolt import App
from backend.slack.blocks import get_incident_modal

def register_commands(app: App):
    @app.command("/incident")
    def handle_incident_command(ack, body, client):
        ack()
        trigger_id = body["trigger_id"]
        try:
            client.views_open(
                trigger_id=trigger_id,
                view=get_incident_modal()
            )
        except Exception as e:
            app.logger.error(f"Error opening modal: {e}")

    @app.view("create_incident_modal")
    def handle_create_incident_view(ack, body, client, view):
        ack()
        
        # Retrieve input values from the view state
        values = view["state"]["values"]
        
        title = values["title_block"]["title_input"]["value"]
        severity = values["severity_block"]["severity_select"]["selected_option"]["value"]
        description = values["description_block"]["description_input"]["value"]
        
        # Create incident
        from backend.services.incident_service import create_incident
        from backend.services.slack_service import post_incident_announcement
        
        incident = create_incident(title, description, severity)
        
        # Announce the incident in the channel
        post_incident_announcement(incident)
