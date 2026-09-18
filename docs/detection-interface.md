```text
Maxwell
Network Monitoring / Preprocessing
        │
        ▼
   NetworkEvent
        │
        ▼
Daniel
Detection Subsystem
 ├── Signature Detection
 └── AI/ML Detection
        │
        ▼
  DetectionResult
        │
        ▼
Truc
Backend / Database / API
        │
        ▼
Terry
Dashboard / Alerts
```

# Detection Interface Specification

## Owner
Daniel Le

## Purpose

This document defines the preliminary Sprint 1 interface between the
network monitoring pipeline, detection subsystem, and backend of the AI-IDS.

These interfaces may be revised as implementation and integration requirements
are verified.

## NetworkEvent

`NetworkEvent` represents standardized network information supplied to the
detection subsystem.

| Field | Type | Description |
|---|---|---|
| event_id | str | Unique identifier for the network event |
| timestamp | datetime | Time associated with the network event |
| src_ip | str | Source IP address |
| dest_ip | str | Destination IP address |
| protocol | str | Network protocol |
| source_port | Optional[int] | Source transport-layer port when applicable; absent for non-port-based protocols such as ICMP |
| destination_port | Optional[int] | Destination transport-layer port when applicable; absent for non-port-based protocols such as ICMP |
| payload_size | int | Size of the network payload |

Current implementation:

`models/network_event.py`

The preliminary Sprint 1 interface originally used a single generic `port`
field. During team integration review, the network monitoring/data pipeline
identified separate source and destination ports in its event contract.
`NetworkEvent` was therefore revised to preserve both values and reduce
ambiguity between client/source ports and destination/service ports.

## DetectionResult

`DetectionResult` represents the result produced after a NetworkEvent is
analyzed by a detection method.

| Field | Type | Description |
|---|---|---|
| event_id | str | Links the result to the original NetworkEvent |
| detected | bool | Indicates whether a potential threat was detected |
| detection_method | str | Detection method used |
| threat_type | Optional[str] | Identified threat category, when applicable |
| severity | Optional[str] | Threat severity, when applicable |
| confidence | Optional[float] | Detection confidence, when applicable |
| timestamp | datetime | Time the detection result was generated |

Current implementation:

`models/detection_result.py`

## Detection Flow

NetworkEvent -> Detection Engine -> DetectionResult

The planned detection engine will support both signature-based and AI/ML-based
detection.

## Integration Responsibilities

Network Monitoring / Data Pipeline:
Produces network data compatible with NetworkEvent.

Detection:
Consumes NetworkEvent and produces DetectionResult.

Backend:
Consumes DetectionResult for processing, storage, API access, and alerting.

## Current Limitations

The current interfaces are preliminary Sprint 1 definitions and may require
additional fields as network capture, detection, and backend integration
requirements are finalized.

Review of the inherited AI-IDS repository identified reusable AI/ML artifacts,
including a Random Forest training notebook, labeled network-traffic datasets,
serialized model artifacts, and a basic inference wrapper. These artifacts are
classified as Partially Implemented because they have not yet been
runtime-validated or integrated with the current Group 7 `NetworkEvent` and
`DetectionResult` interfaces.

The inherited AI/ML implementation also uses a richer flow-level feature set
than the current preliminary `NetworkEvent`. Additional feature extraction or
interface alignment may therefore be required before the inherited model can
be used for live detection.

Review of the inherited project documentation and repository did not identify
a reusable signature-matching engine, signature/rule database, or
Snort/YARA-style rule set. Signature-based detection therefore remains
Not Implemented in the current Group 7 baseline.
