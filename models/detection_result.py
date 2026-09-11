from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DetectionResult:
    """
    Represents the result produced by the detection subsystem
    after analyzing a NetworkEvent.
    """

    event_id: str
    detected: bool
    detection_method: str
    threat_type: Optional[str]
    severity: Optional[str]
    confidence: Optional[float]
    timestamp: datetime
  
