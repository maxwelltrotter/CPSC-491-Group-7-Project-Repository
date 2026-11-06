import os

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

DEFAULT_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]


def register_api_format(app):
    env_origins = os.environ.get("CORS_ORIGINS", "")
    origins = [o.strip() for o in env_origins.split(",") if o.strip()]
    app.config.setdefault("CORS_ORIGINS", origins or DEFAULT_ORIGINS)

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({"error": error.description}), error.code

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")
        if origin and origin in app.config["CORS_ORIGINS"]:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Vary"] = "Origin"
        return response
