from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
    source_port: Optional[int]
    destination_port: Optional[int]
    payload_size: int
