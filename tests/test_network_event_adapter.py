from datetime import datetime, timezone

from scapy.all import Ether, IP, IPv6, TCP, UDP, ICMP, Raw

from capture.network_event_adapter import packet_to_network_event
from detection.signature_detector import detect


def test_tcp_packet_converts_to_network_event():
    packet = (
        IP(src="192.0.2.10", dst="192.0.2.20")
        / TCP(sport=51542, dport=23)
        / Raw(load=b"test")
    )

    packet.time = 1760000000.0

    event = packet_to_network_event(packet)

    assert event is not None
    assert isinstance(event.event_id, str)
    assert event.event_id

    assert event.timestamp == datetime.fromtimestamp(
        1760000000.0, tz=timezone.utc
    )

    assert event.src_ip == "192.0.2.10"
    assert event.dest_ip == "192.0.2.20"
    assert event.protocol == "TCP"
    assert event.source_port == 51542
    assert event.destination_port == 23
    assert event.payload_size == 4



def test_udp_packet_converts_to_network_event():
    packet = (
        IP(src="192.0.2.30", dst="192.0.2.40")
        / UDP(sport=53000, dport=53)
        / Raw(load=b"hello")
    )

    packet.time = 1760000000.0

    event = packet_to_network_event(packet)

    assert event is not None
    assert isinstance(event.event_id, str)
    assert event.event_id
    assert event.timestamp == datetime.fromtimestamp(
        1760000000.0, tz=timezone.utc
    )
    assert event.src_ip == "192.0.2.30"
    assert event.dest_ip == "192.0.2.40"
    assert event.protocol == "UDP"
    assert event.source_port == 53000
    assert event.destination_port == 53
    assert event.payload_size == 5


def test_icmp_packet_converts_without_ports():
    packet = (
        IP(src="192.0.2.50", dst="192.0.2.60")
        / ICMP(type=8)
        / Raw(load=b"ping")
    )

    packet.time = 1760000000.0

    event = packet_to_network_event(packet)

    assert event is not None
    assert event.event_id
    assert event.timestamp == datetime.fromtimestamp(
        1760000000.0, tz=timezone.utc
    )
    assert event.src_ip == "192.0.2.50"
    assert event.dest_ip == "192.0.2.60"
    assert event.protocol == "ICMP"
    assert event.source_port is None
    assert event.destination_port is None
    assert event.payload_size == 4

def test_ipv6_tcp_packet_converts_to_network_event():
    packet = (
        IPv6(src="2001:db8::10", dst="2001:db8::20")
        / TCP(sport=51542, dport=23)
        / Raw(load=b"test")
    )

    packet.time = 1760000000.0

    event = packet_to_network_event(packet)

    assert event is not None
    assert event.event_id
    assert event.timestamp == datetime.fromtimestamp(
        1760000000.0, tz=timezone.utc
    )
    assert event.src_ip == "2001:db8::10"
    assert event.dest_ip == "2001:db8::20"
    assert event.protocol == "TCP"
    assert event.source_port == 51542
    assert event.destination_port == 23
    assert event.payload_size == 4

def test_non_ip_packet_is_ignored():
    packet = Ether(
        src="02:00:00:00:00:01",
        dst="02:00:00:00:00:02",
        type=0x88B5,
    ) / Raw(load=b"unsupported")

    event = packet_to_network_event(packet)

    assert event is None


def test_converted_tcp_packet_triggers_telnet_detection():
    packet = (
        IP(src="192.0.2.10", dst="192.0.2.20")
        / TCP(sport=51542, dport=23)
        / Raw(load=b"test")
    )

    packet.time = 1760000000.0

    event = packet_to_network_event(packet)

    assert event is not None

    result = detect(event)

    assert result.event_id == event.event_id
    assert result.detected is True
    assert result.detection_method == "signature"
    assert result.threat_type == "suspicious_telnet"
    assert result.severity == "medium"
    assert result.confidence is None
    assert result.timestamp == event.timestamp

def test_converted_tcp_packet_triggers_ftp_detection():
    packet = (
        IP(src="192.0.2.10", dst="192.0.2.20")
        / TCP(sport=51542, dport=21)
    )
    packet.time = 1760000000.0

    event = packet_to_network_event(packet)

    assert event is not None

    result = detect(event)

    assert result.event_id == event.event_id
    assert result.detected is True
    assert result.detection_method == "signature"
    assert result.threat_type == "suspicious_ftp"
    assert result.severity == "medium"
    assert result.confidence is None
    assert result.timestamp == event.timestamp


def test_converted_normal_tcp_packet_has_no_detection():
    packet = (
        IP(src="192.0.2.10", dst="192.0.2.20")
        / TCP(sport=51542, dport=443)
    )
    packet.time = 1760000000.0

    event = packet_to_network_event(packet)

    assert event is not None

    result = detect(event)

    assert result.event_id == event.event_id
    assert result.detected is False
    assert result.detection_method == "signature"
    assert result.threat_type is None
    assert result.severity is None
    assert result.confidence is None
    assert result.timestamp == event.timestamp
