from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    """Simple proof-of-life route. If this responds, the backend started ok."""
    return jsonify({"status": "ok"}), 200
