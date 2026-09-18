# For Readable Formatting use link:

https://docs.google.com/document/d/1ihK0LUp9NRYCWgqOdpkR7fYUUCAkTyNEKS0UnMIwXOc/edit?usp=sharing






Network Information Table


Information
Required?
Why?
Downstream use








Timestamp
Yes
Establish when event occurred
Detection, alerts, logging
Source IP
Yes
Identify traffic origin
Detection, alerts, blocking
Destination IP
Yes
Identify traffic target
Detection, alerts
Source port
Yes
Identify originating service/connection
Detection, alerts
Destination port
Yes
Identify destination service
Detection, alerts
Protocol
Yes
Identify traffic type
Detection
Payload size
Yes
Characterize traffic volume
Detection/anomaly analysis




What protocols should be handled by packet capture?
HTTP, HTTPS, TCP/IP, SMTP


Captured packet
      ↓
Ethernet
      ↓
IP
      ↓
TCP
      ↓
HTTP / HTTPS / SMTP



Data Preservation Table

Data
Preserve through detection?
Preserve for alerts/logs?
Timestamp
✓
✓
Source IP
✓
✓
Destination IP
✓
✓
Source port
✓
✓
Destination port
✓
✓
Protocol
✓
✓
Payload size
✓
Possibly




Packet Processing Flow: From Packet Arrival to Detection Send-off


Packet arrives
      ↓
Capture (Scapy)
      ↓
Parse 
      ↓
Preprocess
      ↓
Package into code objects (RawEvent)
      ↓
Send to detection

