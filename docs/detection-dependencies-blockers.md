\# Detection Dependencies \& Blockers



\## Owner



Daniel Le



\## Purpose



This document records the current dependencies, blockers, and unresolved

requirements affecting the AI/ML and signature-based detection subsystem

during Sprint 1.



\## Verified Development Environment



| Dependency | Status | Evidence / Notes |

|---|---|---|

| Python | Verified | Python 3.13.13 |

| pytest | Verified | pytest 9.1.1 |

| Git feature branch | Verified | daniel/sprint1-detection-baseline |

| NetworkEvent | Available | Preliminary detection input model created |

| DetectionResult | Available | Preliminary detection output model created |

| Baseline tests | Verified | 4 tests passed locally |



\## Network Pipeline Dependency



The detection subsystem depends on the Network Monitoring \& Data Pipeline

component to provide network-event data for analysis.



Maxwell's proposed RawEvent structure currently includes:



\- timestamp

\- source\_ip

\- destination\_ip

\- source\_port

\- destination\_port

\- protocol

\- payload\_size



My preliminary NetworkEvent interface currently differs from the proposed

RawEvent structure in field naming and port representation.



The final detection input interface should be aligned with the reviewed

network/preprocessing interface after the network component PR is finalized.



\## Backend Dependency



The detection subsystem produces DetectionResult data that will eventually

be consumed by the backend for processing, storage, API access, and alerting.



The final detection-to-backend integration format has not yet been verified

and will require coordination with the Backend \& API Developer.



## AI/ML Dependencies and Blockers

Current status:

- Trained AI/ML model: Partially Implemented / inherited artifacts verified
- Training code: Verified in inherited repository
- Inference pipeline: Partially Implemented / not yet runtime-validated
- Dataset: Verified in inherited repository
- Required model features: Identified at a high level; exact live feature contract requires validation
- Feature preprocessing requirements: Present in inherited training notebook; live inference compatibility requires validation

Sprint 1 review of the prior AI-IDS repository verified reusable AI/ML
artifacts, including:

- `ai_engine/detector.py`
- `ai_engine/model1.pkl`
- `ai_engine/model2.pkl`
- `notebooks/model_train.ipynb`
- Multiple labeled network-traffic CSV datasets under `data/`

The inherited training notebook uses a Random Forest classifier and includes
dataset loading, preprocessing, train/test splitting, model training, and
evaluation. The inherited inference wrapper uses `joblib` to load a serialized
model and perform classification from an input feature vector.

These artifacts provide a candidate AI/ML baseline for Group 7, but they have
not yet been runtime-validated or integrated with the current `NetworkEvent`
and `DetectionResult` interfaces. The inherited model was trained using a
richer feature set than the current preliminary `NetworkEvent`, so feature
extraction and interface alignment must be addressed before live integration.

Follow-up implementation and validation work is tracked in SCRUM-40.


## Signature Detection Dependencies and Blockers

Current status:

- Signature/rule database: Not Implemented / no reusable inherited implementation identified
- Signature-matching implementation: Not Implemented / no reusable inherited implementation identified
- Signature test cases: Not Implemented
- Threat/severity mappings: Not Implemented

The inherited project documentation defines signature-based detection as part
of the intended AI Engine. However, Sprint 1 review of the prior AI-IDS
repository did not identify a reusable signature-matching engine, signature
database, rule set, or Snort/YARA-style rules.

Group 7 can use the inherited architecture and requirements as guidance, but
the signature-based detection implementation still needs to be developed and
integrated with the current `NetworkEvent` and `DetectionResult` interfaces.

Follow-up implementation work is tracked in SCRUM-39.



\## Resolved Sprint 1 Issue



During initial local testing, pytest failed during test collection because

Python could not resolve the local models package.



The package structure was corrected and the tests were rerun successfully.



Final result:



4 tests passed in 0.08 seconds.



A .gitignore file was also added to prevent generated Python cache files and

local development artifacts from being included in source control.



\## Current Blockers / Unresolved Dependencies

1. Inherited AI/ML artifacts are available but have not yet been runtime-validated
   or integrated into the Group 7 detection pipeline.
2. The inherited AI/ML feature requirements must be aligned with data that can
   be produced by the Group 7 network monitoring/preprocessing component.
3. No reusable inherited signature-detection implementation was identified.
4. Detection input must be aligned with the finalized network-event interface.
5. `DetectionResult` integration requirements must be coordinated with the backend.
6. AI/ML preprocessing and prediction mapping must be validated before the
   inherited model can be used in the Group 7 system.

## Next Actions

- Align `NetworkEvent` with the finalized network/preprocessing contract
  (SCRUM-38).
- Implement the initial signature-based detection engine (SCRUM-39).
- Validate the inherited AI/ML baseline, feature requirements, preprocessing,
  and inference compatibility (SCRUM-40).
- Coordinate `DetectionResult` integration requirements with the backend developer.
- Add integration and detection tests as implementation progresses.

&#x20; Backlog items.

