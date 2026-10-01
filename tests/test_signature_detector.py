from datetime import datetime

from detection.signature_detector import detect
from models.network_event import NetworkEvent


def test_telnet_destination_port_is_detected():
    event_timestamp = datetime.now()

    event = NetworkEvent(
        event_id="event-signature-001",
        timestamp=event_timestamp,
        src_ip="192.168.1.10",
        dest_ip="192.168.1.20",
        protocol="TCP",
        source_port=51542,
        destination_port=23,
        payload_size=128,
    )

    result = detect(event)

    assert result.event_id == event.event_id
    assert result.detected is True
    assert result.detection_method == "signature"
    assert result.threat_type == "suspicious_telnet"
    assert result.severity == "medium"
    assert result.confidence is None
    assert result.timestamp == event_timestamp