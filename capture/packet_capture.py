# This python script captures network packets and logs their details to a file.
# It uses the Scapy library to sniff packets and extract relevant information such as source
# and destination IP addresses, ports, and protocols. Captured data is then written to a log file.

from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, ICMP

# Npcap is a required system-level dependency on Windows 11; installation may be required for packet capture

def process_packet(packet):
    """Display basic packet info from captured traffic"""

    # Record captured timestamp
    timestamp = datetime.now().isoformat(timespec='milliseconds')

    # If packet has IPv4 layer, extract packet information
    if IP in packet:
        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        # Extract protocol information
        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"
        elif ICMP in packet:
            protocol = "ICMP"
        else:
             protocol = f"IPv4 protocol number {packet[IP].proto}"

    # If packet has IPv6 layer
    elif IPv6 in packet:
        source_ip = packet[IPv6].src
        destination_ip = packet[IPv6].dst
        print("-" * 60)
        print(f"Timestamp:       {timestamp}")
        print(f"Source IP:       {source_ip}")
        print(f"Destination IP:  {destination_ip}")
        print("Protocol:        IPv6")
        print(f"Packet Size:     {packet_size} bytes")

    # Else if packet has neither:
    else:
        print("-" * 60)
        print(f"Timestamp:       {timestamp}")
        print("Network Layer:   Non-IP packet")
        print(f"Packet Size:     {packet_size} bytes")
        print("Information:     No IPv4 or IPv6 address available")

    # Get packet size (bytes)
    packet_size = len(packet)

    # Print all captured packet info
    print("-" * 60)
    print(f"Timestamp:       {timestamp}")
    print(f"Source IP:       {source_ip}")
    print(f"Destination IP:  {destination_ip}")
    print(f"Protocol:        {protocol}")
    print(f"Packet Size:     {packet_size} bytes")


def main():
    print("Starting packet capture...")
    print("Capturing 10 packets. Press Ctrl+C to stop early.")

    sniff(prn=process_packet, count=10, store=False)
    print("Packet capture complete.")

if __name__ == "__main__":
    main()



