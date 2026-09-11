from flask_sqlalchemy import SQLAlchemy

# Shared database instance. Imported by app/__init__.py and by every model.
db = SQLAlchemy()
