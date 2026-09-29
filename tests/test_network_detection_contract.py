from datetime import datetime

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