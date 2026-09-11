from dataclasses import dataclass
from datetime import datetime


@dataclass
class NetworkEvent:
    """
    Represents a standardized network event passed from the
    network monitoring pipeline to the detection subsystem.
    """

    event_id: str
    timestamp: datetime
    src_ip: str
    dest_ip: str
    protocol: str
    port: int
    payload_size: int
