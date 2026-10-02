# This python script captures network packets and logs their details to a file.
# It uses the Scapy library to sniff packets and extract relevant information such as source
# and destination IP addresses, ports, and protocols. Captured data is then written to a log file.

from datetime import datetime
import argparse

from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP

# Npcap is a required system-level dependency on Windows 11; installation may be required for packet capture

# Function which processes packets and passes results downstream
def process_packet(packet, downstream_handler=None):
    """Display packet details and pass the packet downstream."""

    # Record captured timestamp and packet length
    timestamp = datetime.now().isoformat(timespec='milliseconds')
    packet_size = len(packet)

    # Set defaults so every packet type can be handled safely.
    source_ip = "N/A"
    destination_ip = "N/A"
    protocol = "Non-IP"

    # Extract network-layer information
    # Handling IP and IPv6 packets
    if IP in packet:
        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"
        elif ICMP in packet:
            protocol = "ICMP"
        else:
            protocol = f"IPv4 protocol number {packet[IP].proto}"

    elif IPv6 in packet:
        source_ip = packet[IPv6].src
        destination_ip = packet[IPv6].dst

        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"
        else:
            protocol = "IPv6"

    # Display summary for every packet (refactored from previous)
    print("-" * 60)
    print(f"Timestamp:       {timestamp}")
    print(f"Source IP:       {source_ip}")
    print(f"Destination IP:  {destination_ip}")
    print(f"Protocol:        {protocol}")
    print(f"Packet Size:     {packet_size} bytes")

    # Pass the original Scapy packet to downstream processing.
    if downstream_handler is not None:
        downstream_handler(packet)

# Main function continuously captures packerts until interrupt
def main(interface=None, downstream_handler=None):
    """Continuously capture packets until interrupted."""

    print("Starting packet capture...")
    print(f"Interface: {interface or 'Scapy default interface'}")
    print("Capturing continuously. Press Ctrl+C to stop.")

    try:
        sniff(
            iface=interface,
            prn=lambda packet: process_packet(
                packet, downstream_handler
            ),
            store=False,
        )

    except KeyboardInterrupt:
        print("\nStopping packet capture...")

    except Exception as error:
        print(f"Packet capture error: {error}")

    finally:
        print("Packet capture complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Continuous Scapy packet capture"
    )
    parser.add_argument(
        "--interface",
        default=None,
        help="Network interface to monitor; uses Scapy's default if omitted",
    )
    args = parser.parse_args()

    # call main
    main(interface=args.interface)
