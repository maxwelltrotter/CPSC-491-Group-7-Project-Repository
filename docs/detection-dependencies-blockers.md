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

| Baseline tests | Verified | 3 tests passed locally |



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



\## AI/ML Dependencies and Blockers



Current status:



\- Trained AI/ML model: Unable to Verify

\- Training code: Unable to Verify

\- Inference pipeline: Unable to Verify

\- Dataset: Unable to Verify

\- Required model features: Unable to Verify

\- Feature preprocessing requirements: Unable to Verify



The current Group 7 repository does not contain a verified inherited AI/ML

implementation. Model-specific implementation and integration decisions

therefore cannot yet be finalized.



\## Signature Detection Dependencies and Blockers



Current status:



\- Signature/rule database: Unable to Verify

\- Signature-matching implementation: Unable to Verify

\- Signature test cases: Unable to Verify

\- Threat/severity mappings: Unable to Verify



The current Group 7 repository does not contain a verified inherited

signature-detection implementation.



\## Resolved Sprint 1 Issue



During initial local testing, pytest failed during test collection because

Python could not resolve the local models package.



The package structure was corrected and the tests were rerun successfully.



Final result:



3 tests passed.



A .gitignore file was also added to prevent generated Python cache files and

local development artifacts from being included in source control.



\## Current Blockers / Unresolved Dependencies



1\. Inherited AI/ML implementation has not been verified.

2\. Inherited signature-detection implementation has not been verified.

3\. Detection input must be aligned with the finalized network-event interface.

4\. DetectionResult integration requirements must be coordinated with the backend.

5\. AI/ML feature requirements cannot be finalized until a model, dataset, or

&#x20;  implementation direction is verified.



\## Next Actions



\- Review the finalized network-event interface after peer review.

\- Align NetworkEvent with the accepted network/preprocessing contract.

\- Coordinate DetectionResult requirements with the backend developer.

\- Determine availability of inherited AI/ML artifacts and datasets.

\- Determine availability of inherited signature/rule implementation.

\- Convert verified missing or incomplete functionality into future Product

&#x20; Backlog items.

