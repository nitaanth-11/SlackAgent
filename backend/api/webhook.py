from flask import Blueprint, request, jsonify
from slack_bolt.adapter.flask import SlackRequestHandler
from backend.slack.client import get_slack_app
from backend.services.incident_service import create_incident
from backend.services.slack_service import post_incident_announcement

webhook_blueprint = Blueprint("webhook", __name__)
_handler = None

def get_handler() -> SlackRequestHandler:
    global _handler
    if _handler is None:
        _handler = SlackRequestHandler(get_slack_app())
    return _handler

@webhook_blueprint.route("/slack/events", methods=["POST"])
def slack_events():
    try:
        handler = get_handler()
        return handler.handle(request)
    except Exception as e:
        # Avoid crashing, print errors
        import logging
        logging.getLogger(__name__).error(f"Error handling Slack request: {e}")
        return jsonify({"error": str(e)}), 500

@webhook_blueprint.route("/api/webhook/alert", methods=["POST"])
def external_alert_webhook():
    try:
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        description = data.get("description", "No description provided.")
        severity = data.get("severity", "medium").lower()
        
        if not title:
            return jsonify({"error": "Missing 'title' field in JSON body."}), 400
            
        if severity not in ["low", "medium", "high", "critical"]:
            severity = "medium"
            
        incident = create_incident(title, description, severity)
        post_incident_announcement(incident)
        
        return jsonify({
            "status": "success",
            "message": "Incident created and announced successfully",
            "incident": incident.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
