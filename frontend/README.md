# AI-IDS Frontend Plan

**Owner:** Terry Li  
**Role:** Frontend, Dashboard & Threat Response Developer  
**Sprint:** Sprint 1 - Goal, Scope, Architecture, and Implementation Planning

## Purpose

This document defines the planned frontend scope for the AI Intrusion Detection System.
The frontend will provide users with a clear interface for viewing network activity,
reviewing threats and alerts, checking system logs, and performing response actions
such as blocking or unblocking suspicious IP addresses.

The frontend will consume data provided by the backend API rather than performing
network monitoring or AI-based threat detection directly.

---

## Frontend Scope

The frontend will contain the following main screens:

### 1. Dashboard

The Dashboard will provide a high-level view of the current state of the AI-IDS system.

Planned information:

- Current network/device status
- Recent security alerts
- Number of detected devices
- Suspicious or malicious devices
- Threat severity information
- Quick access to response actions

### 2. Alerts

The Alerts page will display detected security events.

Each alert should display:

- Timestamp
- Source IP address
- Threat type
- Severity level
- Detection method when available
- Confidence or threat score when available
- Description
- Available user action

Users should be able to view additional information about an alert and take
appropriate actions when necessary.

### 3. Log History

The Log History page will provide a historical record of system activity.

Planned fields include:

- Timestamp
- Event type
- IP address
- Threat type
- Severity
- Description
- Action taken

Future implementation should support filtering or searching logs.

### 4. Ban List

The Ban List will display IP addresses that are currently blocked.

Planned information:

- IP address
- Date/time blocked
- Reason for blocking
- Threat severity
- Current status

The user should be able to request that an IP address be unblocked.

### 5. Settings

The Settings page will provide access to configurable frontend or system options
that are exposed by the backend.

Possible settings include:

- Alert preferences
- Network configuration information
- Logging preferences
- Account-related options

The exact settings will depend on the backend capabilities implemented later
in the project.

---

## Frontend API Data Requirements

The frontend depends on the Backend & API component for system data.

### Alert Data

The frontend should receive:

- Alert ID
- Timestamp
- Source IP address
- Threat type
- Severity
- Description
- Detection method
- Threat/confidence score when available

### Log Data

The frontend should receive:

- Log/event ID
- Timestamp
- Event type
- IP address
- Description
- Threat classification
- Action taken

### Network Device Data

The frontend should receive:

- IP address
- Device identifier or hostname when available
- Connection/status information
- Threat status
- Severity level

### Block/Unblock Actions

For response actions, the frontend will need backend endpoints that allow the user to:

- Request that an IP address be blocked
- Request that an IP address be unblocked
- Receive confirmation that the action succeeded
- Receive an error response if the action failed

The frontend will not directly create firewall rules. It will send the user's request
to the backend and display the result.

---

## Threat and Severity UI Behavior

The frontend will present threat severity consistently throughout the application.

Planned severity levels:

- **Normal:** No known threat detected
- **Low:** Activity worth monitoring but not immediately dangerous
- **Medium:** Suspicious activity that should be reviewed
- **High:** Likely malicious activity requiring attention

Severity should be shown using both text labels and visual indicators so that the
meaning does not depend only on color.

High-risk alerts should be more visually prominent than lower-risk events.

---

## Block and Unblock Interaction

Blocking an IP address is a security-sensitive action, so the user interface should
require confirmation before submitting the request.

Planned block flow:

1. User views a suspicious device or alert.
2. User selects **Block IP**.
3. Frontend displays a confirmation prompt.
4. User confirms the action.
5. Frontend sends the request to the backend API.
6. Frontend displays either a success or error message.
7. The affected views are refreshed.

The unblock flow will follow a similar process.

This approach reduces the chance of accidentally blocking legitimate network traffic.

---

## Frontend States

Frontend screens should account for more than successful responses.

Planned states include:

- Loading
- Successful data retrieval
- Empty data
- API/network error
- Successful response action
- Failed response action

These states will help users understand what the system is doing and prevent unclear
or misleading interface behavior.

---

## Sprint 1 Decisions

During Sprint 1, the following frontend planning decisions were established:

- The primary frontend screens are Dashboard, Alerts, Log History, Ban List, and Settings.
- Threat severity will use consistent Normal, Low, Medium, and High classifications.
- Severity will not rely only on color; text labels will also be displayed.
- Block/unblock actions will require confirmation.
- The frontend will communicate with backend APIs rather than directly controlling
  network monitoring or firewall behavior.
- Backend data requirements were identified before frontend/backend integration begins.

---

## Dependencies

My frontend work depends on other Group 7 components:

### Backend & API Developer

Provides:

- API endpoints
- Alert and log data
- Detection results
- Block/unblock response endpoints

### Network Monitoring & Data Pipeline Developer

Provides:

- Network/device information
- Processed traffic data used by detection components

### AI/ML & Signature Detection Developer

Provides:

- Threat classification
- Severity information
- Detection method
- Detection confidence or threat score when available

---

## Future Sprint Backlog

Planned frontend work includes:

- Implement Dashboard UI
- Implement Alerts page
- Implement Log History page
- Implement Ban List page
- Implement Settings page
- Implement threat severity indicators
- Implement threat details view
- Implement block/unblock controls
- Connect frontend to backend APIs
- Add alert and log filtering
- Add loading, empty, success, and error states
- Perform frontend integration testing
- Perform usability testing
- Finalize UI documentation
- Prepare frontend demonstration flow

---

## Sprint 1 Jira Issues

- SCRUM-18 - Define Frontend Scope and Required Screens
- SCRUM-20 - Define Frontend API Data Requirements
- SCRUM-21 - Define Threat and Severity UI Behavior
- SCRUM-22 - Create Frontend Semester Backlog

---

## Sprint 1 Result

Sprint 1 establishes the frontend requirements and integration expectations needed
before implementation begins. This planning will guide the frontend work in later
sprints and provide clear interfaces between the frontend, backend, network-monitoring,
and detection components.


The AI-IDS will be implemented in Python and run locally on the user’s computer. The frontend will provide a desktop user interface for viewing network activity, alerts, logs, threat severity, and response actions. The frontend will receive data from local backend services through defined interfaces and will not directly perform packet capture, threat detection, or firewall modification.

## Sprint 1 Frontend Skeleton - Run and Test

The Sprint 1 frontend skeleton is a local Tkinter application and is intentionally isolated from unfinished backend, monitoring, detection, and real firewall functionality.

### Run the frontend

From the repository root:

```bash
python -m frontend
```

This launches the Tkinter application through `frontend/__main__.py`.

### Run the mock service tests

From the repository root:

```bash
python -m unittest frontend.tests.test_mock_ids_service
```

The test suite uses Python's built-in `unittest` module. No additional test dependency is required.

### Current integration boundary

The Sprint 1 frontend uses `frontend/services/mock_ids_service.py` and synthetic data in `frontend/data/sample_alerts.json` so the UI can be developed and tested without depending on unfinished backend components. Real monitoring, AI/ML detection, alert generation, and firewall blocking are outside this frontend-only scope.

