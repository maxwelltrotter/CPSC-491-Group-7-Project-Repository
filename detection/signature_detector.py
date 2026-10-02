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

FTP_RULE = SignatureRule(
    name="ftp_destination_port",
    destination_port=21,
    threat_type="suspicious_ftp",
    severity="medium",
)

SIGNATURE_RULES = (
    TELNET_RULE,
    FTP_RULE,
)

def detect(event: NetworkEvent) -> DetectionResult:
    """Evaluate a network event against the baseline signature rules."""

    for rule in SIGNATURE_RULES:
        if event.destination_port == rule.destination_port:
            return DetectionResult(
                event_id=event.event_id,
                detected=True,
                detection_method="signature",
                threat_type=rule.threat_type,
                severity=rule.severity,
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