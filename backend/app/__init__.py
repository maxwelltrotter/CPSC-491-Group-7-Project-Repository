from flask import Flask

from .config import Config
from .extensions import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes.health import health_bp
    from .routes.auth import auth_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    with app.app_context():
        from . import models  # noqa: F401  (registers models before create_all)

        db.create_all()

    return app
