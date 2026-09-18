import datetime

from ..extensions import db


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(64), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    source_ip = db.Column(db.String(45))
    destination_ip = db.Column(db.String(45))
    port = db.Column(db.Integer)
    threat_type = db.Column(db.String(80))
    severity = db.Column(db.String(20))
    detection_method = db.Column(db.String(80))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="new")

    def __repr__(self):
        return f"<Alert {self.alert_id}>"
