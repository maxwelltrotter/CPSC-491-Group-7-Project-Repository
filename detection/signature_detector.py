from dataclasses import dataclass
from models.detection_result import DetectionResult
from models.network_event import NetworkEvent

@dataclass(frozen=True)
class SignatureRule:
    """Represents a metadata-based signature rule."""

    name:str
    destination_port: int
    threat_type: str
    severity: str

TELNET_RULE = SignatureRule(
    name="telnet_destination_port",
    destination_port=23,
    threat_type="suspicious_telnet",
    severity="medium",
)

def detect(event: NetworkEvent) -> DetectionResult:
    """Evaluate a network event against the baseline signature rules."""

    if event.destination_port == TELNET_RULE.destination_port:
        return DetectionResult(
            event_id=event.event_id,
            detected=True,
            detection_method="signature",
            threat_type=TELNET_RULE.threat_type,
            severity=TELNET_RULE.severity,
            confidence=None,
            timestamp=event.timestamp, 
        )
    return DetectionResult(
        event_id=event.event_id, 
        detected=False,
        detection_method="signature",
        threat_type=None,
        severity=None,
        confidence=None,
        timestamp=event.timestamp,
    )