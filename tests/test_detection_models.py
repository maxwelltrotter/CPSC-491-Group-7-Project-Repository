from datetime import datetime

from models.network_event import NetworkEvent
from models.detection_result import DetectionResult


def test_network_event_creation():
    event = NetworkEvent(
        event_id="event-001",
        timestamp=datetime.now(),
        src_ip="192.168.1.10",
        dest_ip="192.168.1.20",
        protocol="TCP",
        port=443,
        payload_size=512,
    )

    assert event.event_id == "event-001"
    assert event.src_ip == "192.168.1.10"
    assert event.dest_ip == "192.168.1.20"
    assert event.protocol == "TCP"
    assert event.port == 443
    assert event.payload_size == 512


def test_detection_result_creation():
    result = DetectionResult(
        event_id="event-001",
        detected=True,
        detection_method="signature",
        threat_type="test-threat",
        severity="medium",
        confidence=None,
        timestamp=datetime.now(),
    )

    assert result.event_id == "event-001"
    assert result.detected is True
    assert result.detection_method == "signature"
    assert result.threat_type == "test-threat"
    assert result.severity == "medium"
    assert result.confidence is None


def test_network_event_without_port():
    event = NetworkEvent(
        event_id="event-003",
        timestamp=datetime.now(),
        src_ip="10.0.0.1",
        dest_ip="10.0.0.2",
        protocol="ICMP",
        port=None,
        payload_size=64,
    )

    assert event.protocol == "ICMP"
    assert event.port is None


def test_clean_detection_result():
    result = DetectionResult(
        event_id="event-002",
        detected=False,
        detection_method="signature",
        threat_type=None,
        severity=None,
        confidence=None,
        timestamp=datetime.now(),
    )

    assert result.detected is False
    assert result.threat_type is None
    assert result.severity is None
