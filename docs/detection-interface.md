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
| port | int | Relevant network/service port |
| payload_size | int | Size of the network payload |

Current implementation:

`models/network_event.py`

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

The current interfaces are preliminary Sprint 1 definitions.

The current group repository does not contain a verified inherited AI/ML model,
inference pipeline, signature database, or signature matching implementation.
Those components remain Unable to Verify.

Additional fields may be required after network capture, AI/ML, signature, and
backend requirements are further evaluated.
