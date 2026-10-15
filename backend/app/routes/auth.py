from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models.user import User
from ..validators import check_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not username.strip():
        return jsonify({"error": "Username is required."}), 400
    username = username.strip()
    if len(username) > 80:
        return jsonify({"error": "Username is too long."}), 400

    problems = check_password(password)
    if problems:
        return jsonify({"error": "Password is too weak.", "details": problems}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "That username is already taken."}), 409

    user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered.", "username": user.username}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Sprint 1 stub: just proves the route exists and returns the right shape.
    Sprint 2 adds: real credential check, session/token creation, failed-
    attempt tracking, and lockout after 5 bad tries.
    """
    data = request.get_json(silent=True) or {}
    return jsonify({"message": "login endpoint reached", "received": data}), 200
