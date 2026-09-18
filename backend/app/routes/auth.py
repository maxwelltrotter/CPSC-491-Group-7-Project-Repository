from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Sprint 1 stub: just proves the route exists and returns the right shape.
    Sprint 2 adds: duplicate-username check, password complexity check,
    password hashing, real user creation, and audit logging.
    """
    data = request.get_json(silent=True) or {}
    return jsonify({"message": "register endpoint reached", "received": data}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Sprint 1 stub: just proves the route exists and returns the right shape.
    Sprint 2 adds: real credential check, session/token creation, failed-
    attempt tracking, and lockout after 5 bad tries.
    """
    data = request.get_json(silent=True) or {}
    return jsonify({"message": "login endpoint reached", "received": data}), 200
