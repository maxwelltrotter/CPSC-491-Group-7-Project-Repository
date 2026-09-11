from flask import Flask

from .config import Config
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes.health import health_bp
    from .routes.auth import auth_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    with app.app_context():
        from . import models  # noqa: F401  (registers models before create_all)

        db.create_all()

    return app
