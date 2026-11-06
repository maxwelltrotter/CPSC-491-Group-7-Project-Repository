from functools import wraps

from flask import Blueprint, g, jsonify, request, current_app
from itsdangerous import BadSignature, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

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


MAX_FAILED_ATTEMPTS = 5
TOKEN_MAX_AGE = 3600  # one hour, in seconds


def make_token(user):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps({"user_id": user.id})


def token_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "Login required."}), 401

        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(header[len("Bearer "):], max_age=TOKEN_MAX_AGE)
        except BadSignature:
            return jsonify({"error": "Invalid or expired token."}), 401

        user = db.session.get(User, data.get("user_id"))
        if user is None:
            return jsonify({"error": "Invalid or expired token."}), 401

        g.current_user = user
        return view(*args, **kwargs)

    return wrapper


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    bad_login = jsonify({"error": "Invalid username or password."}), 401

    if not isinstance(username, str) or not isinstance(password, str):
        return bad_login

    user = User.query.filter_by(username=username.strip()).first()
    if user is None:
        return bad_login

    if user.locked:
        return jsonify({"error": "This account is locked."}), 423

    if not check_password_hash(user.password_hash, password):
        user.failed_attempts += 1
        if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked = True
        db.session.commit()
        return bad_login

    user.failed_attempts = 0
    db.session.commit()
    return jsonify({
        "message": "Login successful.",
        "username": user.username,
        "access_token": make_token(user),
    }), 200


@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    return jsonify({"username": g.current_user.username}), 200
