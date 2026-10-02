# Frontend Testing

## Purpose

This document explains how to run the frontend automated tests locally and how
they are expected to participate in the project's shared CI process. The tests
use `unittest`-style classes but are collected and executed through `pytest`.

## Prerequisites

Run all commands from the repository root. The project targets Python 3.12.

Install the project dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Test Commands

Run only the frontend mock IDS service tests:

```bash
python -m pytest frontend/tests/test_mock_ids_service.py -q
```

Run the complete repository test suite:

```bash
python -m pytest -q
```

## Current Frontend Test Coverage

The current frontend test suite covers:

- Required alert fields across all returned alerts
- Supported severity values
- Numeric confidence values between 0 and 1 inclusive
- Mock block and unblock happy-path behavior
- Rejection of blank and duplicate block requests
- Rejection of unblock requests for unknown IP addresses
- Dashboard alert, banned-IP, and severity counts
- Defensive-copy behavior for returned alert and banned-IP data

## Scope and Limitations

The Sprint 2 frontend tests are limited to the frontend service layer and mock
IDS behavior. They do not:

- Interact with the real system firewall
- Capture or process live network packets
- Implement or test detection or machine-learning logic
- Implement or test backend functionality
- Perform full Tkinter GUI automation

Frontend-backend integration testing and Tkinter startup testing remain future
work.

## Shared CI Integration

The group-standardized test command is:

```bash
python -m pytest
```

The frontend tests are structured so that this repository-wide command
automatically discovers them. The group-level GitHub Actions workflow should use
the same command. This document does not claim that the shared workflow has
already been implemented, and a separate frontend-specific workflow should not
be created.

## Warning Note

Repository-wide test execution may display a `CryptographyDeprecationWarning`
from Scapy and its third-party cryptography dependency. The warning does not
replace a successful test result: pytest must still exit successfully. Changing
dependencies only to suppress this warning is outside the frontend Sprint 2
scope.

## Verified Local Results

At commit `0b0f82c` on branch `terry/sprint2-frontend-tests`, these local results
were verified:

- Frontend test suite: `9 passed`
- Full repository test suite: `15 passed, 1 warning`
- The warning was the third-party Scapy `CryptographyDeprecationWarning`

These are local results and do not claim that the shared GitHub Actions workflow
has already run.

## Troubleshooting

### Wrong Working Directory

Run pytest from the repository root so package imports and project paths resolve
correctly. Verify the root with:

```bash
git rev-parse --show-toplevel
```

### Missing Dependencies

Install the project requirements and verify pytest:

```bash
python -m pip install -r requirements.txt
python -m pytest --version
```

### Test Collection Problems

Inspect frontend and repository-wide collection with:

```bash
python -m pytest frontend/tests/test_mock_ids_service.py --collect-only -q
python -m pytest --collect-only -q
```

### Test Failures and Warnings

A test failure means an assertion or required behavior did not pass and should
be investigated before merging. A warning does not automatically mean that a
test run failed or passed; always confirm the final pytest result and exit
status.

## Sprint 2 Tracking

- [SCRUM-42](https://cpsc491-05-group-07.atlassian.net/browse/SCRUM-42) - Add Frontend Tests to Shared CI Pipeline
- [SCRUM-43](https://cpsc491-05-group-07.atlassian.net/browse/SCRUM-43) - Expand Frontend Service Contract and Severity Tests
- [SCRUM-44](https://cpsc491-05-group-07.atlassian.net/browse/SCRUM-44) - Document Frontend CI Commands and Test Scope
- [Pull Request #9](https://github.com/maxwelltrotter/CPSC-491-Group-7-Project-Repository/pull/9) - `terry/sprint2-frontend-tests` into `main`
