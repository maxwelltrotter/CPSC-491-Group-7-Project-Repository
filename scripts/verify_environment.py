import sys

from scapy.all import IP, TCP
from dotenv import load_dotenv


def main():
    load_dotenv()

    print("Environment verification")
    print("------------------------")
    print(f"Python version: {sys.version.split()[0]}")

    packet = IP(src="192.168.1.10", dst="192.168.1.20") / TCP(
        sport=12345,
        dport=80
    )

    print("Scapy import: OK")
    print(f"Test packet source: {packet.src}")
    print(f"Test packet destination: {packet.dst}")
    print(f"Test packet protocol: TCP")
    print("Environment is ready")


if __name__ == "__main__":
    main()
