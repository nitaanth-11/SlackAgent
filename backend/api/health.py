from flask import Blueprint, jsonify

health_blueprint = Blueprint("health", __name__)

@health_blueprint.route("/health", methods=["GET"])
@health_blueprint.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "OpsPilot Backend"
    }), 200
