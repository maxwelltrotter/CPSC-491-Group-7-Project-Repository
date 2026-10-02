
# This python script captures network packets and logs their details to a file.
# It uses the Scapy library to sniff packets and extract relevant information such as source
# and destination IP addresses, ports, and protocols. Captured data is then written to a log file.

import time # DEBUG
import argparse
import json
import logging
from datetime import datetime
from pathlib import Path

# Npcap is a required system-level dependency on Windows 11; installation may be required for packet capture
from scapy.all import AsyncSniffer, sniff, IP, IPv6, TCP, UDP, ICMP, get_if_list

# Default configuration
DEFAULT_CONFIG = {
    "interface": None,
    "filter": "",
    "timeout": None,
    "packet_count": 0,
    "log_file": "logs/packet_capture.log",
}

# Configure logging functionality
def setup_logging(log_file):
    """Configure logging to both a file and the console."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )

# Load capture config settings from json
def load_config(config_path):
    """Load capture settings and apply defaults."""
    path = Path(config_path)

    try:
        with path.open("r", encoding="utf-8") as config_file:
            user_config = json.load(config_file)
    except FileNotFoundError:
        logging.warning(
            "Configuration file %s not found; using defaults.", path
        )
        user_config = {}
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in configuration file {path}: {error}"
        ) from error

    if not isinstance(user_config, dict):
        raise ValueError("Capture configuration must be a JSON object.")

    config = {**DEFAULT_CONFIG, **user_config}
    validate_config(config)
    return config

# Validate configuration pre-capture
def validate_config(config):
    """Validate configuration values before starting capture."""
    interface = config["interface"]
    if interface is not None and (
        not isinstance(interface, str) or not interface.strip()
    ):
        raise ValueError("'interface' must be a non-empty string or null.")

    capture_filter = config["filter"]
    if not isinstance(capture_filter, str):
        raise ValueError("'filter' must be a string.")

    timeout = config["timeout"]
    if timeout is not None and (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise ValueError("'timeout' must be a positive number or null.")

    packet_count = config["packet_count"]
    if (
        isinstance(packet_count, bool)
        or not isinstance(packet_count, int)
        or packet_count < 0
    ):
        raise ValueError("'packet_count' must be a non-negative integer.")

    if not isinstance(config["log_file"], str) or not config["log_file"]:
        raise ValueError("'log_file' must be a non-empty string.")

# Validate interface
def validate_interface(interface):
    """Check that an explicitly configured interface exists."""
    if interface is None:
        return

    try:
        interfaces = get_if_list()
    except Exception as error:
        raise RuntimeError(
            f"Could not retrieve network interfaces: {error}"
        ) from error

    if interface not in interfaces:
        raise ValueError(
            f"Interface '{interface}' is unavailable. "
            f"Available interfaces: {', '.join(interfaces) or 'none'}"
        )

# Start Network Traffic Capture; throw errors gracefully
def start_capture(config, downstream_handler=None):
    interface = config["interface"]
    packet_count = config["packet_count"]

    sniffer = AsyncSniffer(
        iface=interface,
        filter=config["filter"] or None,
        timeout=config["timeout"],
        count=packet_count,
        prn=lambda packet: process_packet(
            packet, downstream_handler
        ),
        store=False,
    )

    try:
        logging.info(
            "Starting packet capture (interface=%s, filter=%r, "
            "timeout=%s, packet_count=%s).",
            interface or "default",
            config["filter"],
            config["timeout"],
            packet_count or "unlimited",
        )

        sniffer.start()

        # Keep the main thread alive while capture runs.
        while sniffer.running:
            time.sleep(0.2)

        logging.info("Packet capture finished.")

    except KeyboardInterrupt:
        logging.warning("Ctrl+C received. Stopping packet capture.")

        if sniffer.running:
            sniffer.stop()

        logging.info("Packet capture stopped by user.")

    except Exception:
        logging.exception("Packet capture failed.")

        if sniffer.running:
            try:
                sniffer.stop()
            except Exception:
                logging.exception("Failed to stop packet capture cleanly.")

    finally:
        logging.info("Capture session ended.")

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
def main():
    parser = argparse.ArgumentParser(
        description="Configurable Scapy packet capture"
    )
    parser.add_argument(
        "--config",
        default="config/packet_capture.json",
        help="Path to the capture JSON configuration",
    )
    parser.add_argument(
        "--interface",
        help="Override the configured interface",
    )
    parser.add_argument(
        "--filter",
        dest="capture_filter",
        help="Override the configured BPF filter",
    )
    args = parser.parse_args()

    try:
        logging.basicConfig(level=logging.INFO)

        config = load_config(args.config)

        if args.interface is not None:
            config["interface"] = args.interface
        if args.capture_filter is not None:
            config["filter"] = args.capture_filter

        validate_config(config)
        setup_logging(config["log_file"])
        start_capture(config)

    except (ValueError, OSError, RuntimeError) as error:
        logging.error("Unable to configure packet capture: %s", error)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
