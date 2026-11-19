"""Read-only checks for the bundled, synthetic frontend demonstration data."""

from pathlib import Path

from .services.mock_ids_service import MockIDSService


EXPECTED_DEMO_ALERT_IDS = frozenset({"ALT-001", "ALT-002", "ALT-003"})


def check_demo_data(data_path: str | Path | None = None) -> dict[str, object]:
    """Fail if the mock fixture no longer supports the documented three-alert demo."""
    service = MockIDSService(data_path)
    alerts = service.get_alerts()
    alert_ids = [alert["alert_id"] for alert in alerts]
    if len(alert_ids) != len(set(alert_ids)):
        raise ValueError("demo alerts contain duplicate IDs")
    if set(alert_ids) != EXPECTED_DEMO_ALERT_IDS:
        raise ValueError("demo alerts must contain ALT-001, ALT-002, and ALT-003")

    summary = service.get_dashboard_summary()
    if summary["active_alert_count"] != len(alerts):
        raise ValueError("dashboard alert count differs from demo alert data")
    if sum(summary["severity_counts"].values()) != len(alerts):
        raise ValueError("dashboard severity counts differ from demo alert data")

    return {"alert_count": len(alerts), "alert_ids": alert_ids}
