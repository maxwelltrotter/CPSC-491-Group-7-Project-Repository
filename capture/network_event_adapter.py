from datetime import datetime, timezone
from uuid import uuid4

from scapy.all import IP, IPv6, TCP, UDP, ICMP, Raw

from models.network_event import NetworkEvent


def packet_to_network_event(packet) -> NetworkEvent | None:
    """Convert a supported Scapy packet into a NetworkEvent."""

    # Identify the network layer.
    if IP in packet:
        network_layer = packet[IP]
    elif IPv6 in packet:
        network_layer = packet[IPv6]
    else:
        # Ignore packets without an IPv4 or IPv6 layer.
        return None

    source_port = None
    destination_port = None

    # Identify the transport protocol and applicable ports.
    if TCP in packet:
        protocol = "TCP"
        source_port = int(packet[TCP].sport)
        destination_port = int(packet[TCP].dport)

    elif UDP in packet:
        protocol = "UDP"
        source_port = int(packet[UDP].sport)
        destination_port = int(packet[UDP].dport)

    elif ICMP in packet:
        protocol = "ICMP"

    else:
        # Unsupported transport protocol for this baseline.
        return None

    # Preserve the packet's recorded timestamp.
    timestamp = datetime.fromtimestamp(
        float(packet.time),
        tz=timezone.utc,
    )

    # Count application payload bytes, not total packet bytes.
    payload_size = len(bytes(packet[Raw].load)) if Raw in packet else 0

    return NetworkEvent(
        event_id=str(uuid4()),
        timestamp=timestamp,
        src_ip=str(network_layer.src),
        dest_ip=str(network_layer.dst),
        protocol=protocol,
        source_port=source_port,
        destination_port=destination_port,
        payload_size=payload_size,
    )
