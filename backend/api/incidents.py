from flask import Blueprint, jsonify, abort
from backend.services.incident_service import list_incidents, get_incident

incidents_blueprint = Blueprint("incidents", __name__)

@incidents_blueprint.route("/api/incidents", methods=["GET"])
def get_all_incidents():
    try:
        incidents = list_incidents()
        return jsonify([inc.to_dict() for inc in incidents]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@incidents_blueprint.route("/api/incidents/<int:incident_id>", methods=["GET"])
def get_single_incident(incident_id):
    try:
        incident = get_incident(incident_id)
        if not incident:
            return jsonify({"error": f"Incident with ID {incident_id} not found."}), 404
        return jsonify(incident.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
