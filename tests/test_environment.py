import sys

from scapy.all import IP, TCP


def test_python_version():
    assert sys.version_info >= (3, 12)


def test_scapy_can_construct_packet():
    packet = IP(src="192.168.1.10", dst="192.168.1.20") / TCP(
        sport=12345,
        dport=80
    )

    assert packet.src == "192.168.1.10"
    assert packet.dst == "192.168.1.20"
    assert packet.sport == 12345
    assert packet.dport == 80
