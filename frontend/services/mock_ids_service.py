from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ids_service import IDSService


class MockIDSService(IDSService):
    """Mock IDS service used for frontend development before backend integration."""

    _REQUIRED_ALERT_FIELDS = frozenset(
        {
            "alert_id",
            "timestamp",
            "source_ip",
            "threat_type",
            "severity",
            "detection_method",
            "confidence",
            "description",
        }
    )
    _SUPPORTED_SEVERITIES = frozenset({"Normal", "Low", "Medium", "High"})
    _REVIEW_DISPOSITIONS = frozenset(
        {"Confirmed incident", "False positive", "Needs investigation"}
    )

    def __init__(self, data_path: str | Path | None = None) -> None:
        if data_path is None:
            data_path = Path(__file__).resolve().parent.parent / "data" / "sample_alerts.json"
        self._data_path = Path(data_path)
        self._alerts = self._load_alerts()
        self._alert_reviews: list[dict[str, Any]] = []
        self._banned_ips: list[dict[str, Any]] = [
            {
                "ip_address": "198.51.100.42",
                "blocked_at": "2026-09-17T18:40:00",
                "reason": "Repeated suspicious connection attempts",
                "severity": "High",
            }
        ]
        self._settings: dict[str, Any] = {
            "alerts_enabled": True,
            "logging_enabled": True,
            "network_interface": "Mock Interface",
        }

    def _load_alerts(self) -> list[dict[str, Any]]:
        with self._data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("sample_alerts.json must contain a JSON array")

        for index, alert in enumerate(data):
            self._validate_alert(alert, index)
        return data

    @classmethod
    def _validate_alert(cls, alert: object, index: int) -> None:
        if not isinstance(alert, dict):
            raise ValueError(f"alert at index {index} must be a JSON object")

        missing_fields = cls._REQUIRED_ALERT_FIELDS.difference(alert)
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"alert at index {index} is missing required fields: {missing}")

        severity = alert["severity"]
        if severity not in cls._SUPPORTED_SEVERITIES:
            raise ValueError(f"alert at index {index} has unsupported severity: {severity}")

        confidence = alert["confidence"]
        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0 <= confidence <= 1
        ):
            raise ValueError(
                f"alert at index {index} confidence must be a number between 0 and 1"
            )

    def get_dashboard_summary(self) -> dict[str, Any]:
        severity_counts = {"Normal": 0, "Low": 0, "Medium": 0, "High": 0}
        for alert in self._alerts:
            severity = str(alert.get("severity", "Normal"))
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            "device_count": 6,
            "active_alert_count": len(self._alerts),
            "banned_ip_count": len(self._banned_ips),
            "severity_counts": severity_counts,
        }

    def get_alerts(self) -> list[dict[str, Any]]:
        return deepcopy(self._alerts)

    def get_alert_reviews(self) -> list[dict[str, Any]]:
        return deepcopy(self._alert_reviews)

    def review_alert(
        self,
        alert_id: str,
        disposition: str,
        reason: str,
        reviewer: str,
        next_action: str = "",
        owner: str = "",
    ) -> dict[str, Any]:
        if not any(alert["alert_id"] == alert_id for alert in self._alerts):
            raise ValueError(f"unknown alert ID: {alert_id}")
        if disposition not in self._REVIEW_DISPOSITIONS:
            raise ValueError(f"unsupported alert disposition: {disposition}")
        if not reason.strip():
            raise ValueError("review reason is required")
        if not reviewer.strip():
            raise ValueError("reviewer is required")

        requires_follow_up = disposition in {
            "Confirmed incident",
            "Needs investigation",
        }
        if requires_follow_up and not next_action.strip():
            raise ValueError("next action is required for this disposition")
        if requires_follow_up and not owner.strip():
            raise ValueError("follow-up owner is required for this disposition")

        review = {
            "alert_id": alert_id,
            "disposition": disposition,
            "reason": reason.strip(),
            "reviewer": reviewer.strip(),
            "reviewed_at": datetime.now(timezone.utc).isoformat(),
            "next_action": next_action.strip(),
            "owner": owner.strip(),
            "status": "Closed" if disposition == "False positive" else "Open",
            "data_source": "Mock/Synthetic",
        }
        self._alert_reviews.append(review)
        return deepcopy(review)

    def get_logs(self) -> list[dict[str, Any]]:
        return [
            {
                "timestamp": alert["timestamp"],
                "event_type": "Security Alert",
                "ip_address": alert["source_ip"],
                "description": alert["description"],
                "severity": alert["severity"],
                "action_taken": "Pending review",
            }
            for alert in self._alerts
        ]

    def get_banned_ips(self) -> list[dict[str, Any]]:
        return deepcopy(self._banned_ips)

    def block_ip(self, ip_address: str) -> dict[str, Any]:
        if not ip_address.strip():
            return {"success": False, "message": "IP address is required."}

        if any(item["ip_address"] == ip_address for item in self._banned_ips):
            return {"success": False, "message": f"{ip_address} is already on the mock ban list."}

        self._banned_ips.append(
            {
                "ip_address": ip_address,
                "blocked_at": "mock-now",
                "reason": "Mock user action",
                "severity": "Manual",
            }
        )
        return {"success": True, "message": f"Mock block request succeeded for {ip_address}."}

    def unblock_ip(self, ip_address: str) -> dict[str, Any]:
        for index, item in enumerate(self._banned_ips):
            if item["ip_address"] == ip_address:
                del self._banned_ips[index]
                return {"success": True, "message": f"Mock unblock request succeeded for {ip_address}."}
        return {"success": False, "message": f"{ip_address} is not on the mock ban list."}

    def get_settings(self) -> dict[str, Any]:
        return deepcopy(self._settings)
