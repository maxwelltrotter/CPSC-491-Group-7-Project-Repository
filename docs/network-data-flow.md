# Network Monitoring & Data Pipeline — Architecture Review

## 1. Purpose

The Network Monitoring/Data Pipeline component is responsible for capturing network traffic, extracting relevant network information, preprocessing the captured data, and producing standardized event data that can be consumed by the AI-IDS detection engine.

## 2. Position in the System

The Network Monitoring/Data Pipeline is **positioned between the network environment and the detection engine**:

                    NETWORK
                      │
                      ▼
              ┌─────────────────┐
              │ Packet Capture  │
              │     Scapy       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Packet Parser   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Preprocessing  │
              │  / Normalizing  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    RawEvent     │
              └────────┬────────┘
                       │
             ┌─────────┴──────────┐
             ▼                    ▼
      ┌──────────────┐     ┌───────────────┐
      │ AI/ML Model  │     │   Signature   │
      │   Detection  │     │   Detection   │
      └──────┬───────┘     └───────┬───────┘
             │                     │
             └──────────┬──────────┘
                        ▼
                ┌───────────────┐
                │ Backend / API │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   Dashboard   │
                │ / Response    │
                └───────────────┘

**Data Flow:**

Network Traffic --> Packet Capture *(Scapy)* --> Packet Processing --> Data Preprocessing / Normalization --> RawEvent --> Detection Engine --> Backend/API --> Dashboard / Threat Response

## 3. Network Traffic Input

The component uses **Scapy** as the packet-capture technology.

The captured packet information relevant to the IDS includes:

* Timestamp
* Source IP address
* Destination IP address
* Source port
* Destination port
* Protocol
* Payload size

## 4. Processing Responsibilities

The Network Monitoring/Data Pipeline is responsible for:

1. Capturing network packets.
2. Extracting relevant packet information.
3. Cleaning and validating captured data.
4. Normalizing data into a consistent format.
5. Preparing data required by the detection engine.
6. Creating standardized `RawEvent` objects.
7. Passing `RawEvent` data to the detection engine.
8. Providing sufficient network context for downstream alerts and logging.

## 5. RawEvent

`RawEvent` is the primary data contract between the Network Monitoring/Data Pipeline and the detection engine.

The exact fields should be finalized with the AI/ML and Backend developers before implementation.

Initial expected information includes:

* Timestamp
* Source IP
* Destination IP
* Source port
* Destination port
* Protocol
* Payload size
* Additional detection-related features as required

## 6. Connection to the Detection Engine

The Network Monitoring/Data Pipeline provides the input data used by the detection engine.

The detection engine uses network information for two primary detection approaches:

### Signature-Based Detection

The system is expected to identify known attack patterns, including examples such as:

* SQL injection
* Port scanning
* DDoS activity

### Anomaly-Based Detection

The system is also expected to identify unusual network behavior, such as:

* Traffic spikes
* Uncommon interactions
* Deviations from expected traffic behavior

Therefore, the pipeline must provide clean and consistently structured network data that can be used by both detection approaches.

## 7. Connection to Backend

The Backend component consumes detection results and supports communication with the frontend/dashboard.

The Network Monitoring/Data Pipeline therefore does not need to own the user interface or business-level response logic.

Its primary responsibility is to provide reliable network/event data to the downstream system.

The pipeline should coordinate with the Backend developer to establish:

* Event format
* Data types
* API/interface expectations
* Error handling
* Logging requirements
* How network information is preserved in detection results and alerts

## 8. Dependencies

### AI/ML Developer

The Network Monitoring/Data Pipeline depends on the AI/ML developer to determine:

* Which network features are required by the model
* Expected input data types
* Required preprocessing
* Expected `RawEvent` structure
* How the model receives network events

### Backend Developer

The Network Monitoring/Data Pipeline depends on the Backend developer to determine:

* How events are transferred between components
* API/interface requirements
* Data persistence requirements
* Alert/log data requirements
* Error-handling expectations

## 9. Open Questions

The following questions should be resolved before implementation:

1. What exact fields must `RawEvent` contain?
2. Which fields are required by the AI/ML model?
3. Which fields are required for signature detection?
4. Where does preprocessing occur?
5. How is `RawEvent` passed to the detection engine?
6. Does the backend receive raw events, detection results, or both?
7. Where are network events stored?
8. What happens when packet capture fails?
9. What happens when a packet contains missing or invalid information?
10. What latency is expected between packet capture and detection?

## 10. Definition of Completion

This architecture-review task is complete when:

* The Network Monitoring/Data Pipeline's position in the system is documented.
* Inputs and outputs are identified.
* `RawEvent` is defined at an initial level.
* AI/ML dependencies are documented.
* Backend dependencies are documented.
* Open interface questions are identified.
* The team agrees on the data flow before implementation begins.
