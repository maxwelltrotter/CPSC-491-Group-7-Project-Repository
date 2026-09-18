# This file proposes a data structure for the RawEvent class.
# This class is used to create objects of the RawEvent type, which will contain
# packet information captured directly from the network. These objects will be
# subjected to data preprocessing, and later signature/AI-ML based threat detection.

# Class definition for RawEvent
class RawEvent:
    def __init__(
            self,
            timestamp,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            protocol,
            payload_size
            ): 
        
        self.timestamp = timestamp
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.source_port = source_port
        self.destination_port = destination_port
        self.protocol = protocol
        self.payload_size = payload_size
    def __dict__(self):
        return {
            "timestamp": self.timestamp,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "source_port": self.source_port,
            "destination_port": self.destination_port,
            "protocol": self.protocol,
            "payload_size": self.payload_size
        }

def main():

    # Create a demo instance of RawEvent
    demo_event = RawEvent(
        timestamp="2024-06-01T12:00:00Z",
        source_ip="192.168.1.1",
        destination_ip="192.168.1.2",
        source_port=12345,
        destination_port=80,
        protocol="TCP",
        payload_size=1024
    )
    print("Test RawEvent Object has attributes:")
    print(demo_event.__dict__())
    exit(0)

if __name__ == "__main__":
    main()

