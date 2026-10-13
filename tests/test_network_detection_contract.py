from datetime import datetime

from datetime import datetime

from detection.signature_detector import detect
from models.detection_result import DetectionResult
from models.network_event import NetworkEvent



def test_representative_network_data_matches_detection_contract():
    upstream_data = {
        "event_id": "event-contract-001",
        "timestamp": datetime.now(),
        "src_ip": "192.168.1.10",
        "dest_ip": "192.168.1.20",
        "protocol": "TCP",
        "source_port": 51542,
        "destination_port": 443,
        "payload_size": 512,
    }

    event = NetworkEvent(**upstream_data)

    assert event.event_id == upstream_data["event_id"]
    assert event.src_ip == upstream_data["src_ip"]
    assert event.dest_ip == upstream_data["dest_ip"]
    assert event.protocol == upstream_data["protocol"]
    assert event.source_port == upstream_data["source_port"]
    assert event.destination_port == upstream_data["destination_port"]
    assert event.payload_size == upstream_data["payload_size"]


def test_matching_event_produces_valid_detection_result():
    event_timestamp = datetime.now()

    event = NetworkEvent(
        event_id="event-contract-detection-001",
        timestamp=event_timestamp,
        src_ip="192.168.1.10",
        dest_ip="192.168.1.20",
        protocol="TCP",
        source_port=51542,
        destination_port=23,
        payload_size=128,
    )

    result = detect(event)

    assert isinstance(result, DetectionResult)
    assert result.event_id == event.event_id
    assert result.timestamp == event.timestamp
    assert isinstance(result.detected, bool)
    assert result.detected is True
    assert result.detection_method == "signature"
    assert result.threat_type == "suspicious_telnet"
    assert result.severity == "medium"
    assert result.confidence is None


def test_portless_icmp_event_produces_valid_detection_result():
    event_timestamp = datetime.now()

    event = NetworkEvent(
        event_id="event-contract-icmp-001",
        timestamp=event_timestamp,
        src_ip="192.168.1.10",
        dest_ip="192.168.1.20",
        protocol="ICMP",
        source_port=None,
        destination_port=None,
        payload_size=64,
    )

    result = detect(event)

    assert isinstance(result, DetectionResult)
    assert result.event_id == event.event_id
    assert result.timestamp == event_timestamp
    assert result.detected is False
    assert result.detection_method == "signature"
    assert result.threat_type is None
    assert result.severity is None
    assert result.confidence is None
