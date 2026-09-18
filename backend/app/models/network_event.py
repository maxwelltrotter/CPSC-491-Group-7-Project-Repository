import datetime

from ..extensions import db


class NetworkEvent(db.Model):
    __tablename__ = "network_events"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(64), unique=True, nullable=False)
    session_id = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    source_ip = db.Column(db.String(45))
    destination_ip = db.Column(db.String(45))
    protocol = db.Column(db.String(20))
    port = db.Column(db.Integer)
    payload_size = db.Column(db.Integer)

    def __repr__(self):
        return f"<NetworkEvent {self.event_id}>"
