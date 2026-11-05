from __future__ import annotations

import json
import tempfile
import unittest
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from frontend.services.mock_ids_service import MockIDSService


def workspace_temporary_directory() -> tempfile.TemporaryDirectory:
    """Create temporary test data inside the writable repository workspace."""
    return tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2])


class MockIDSServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = MockIDSService()

    def test_get_alerts_returns_expected_shape(self) -> None:
        alerts = self.service.get_alerts()
        self.assertGreater(len(alerts), 0)

        required_fields = {
            "alert_id",
            "timestamp",
            "source_ip",
            "threat_type",
            "severity",
            "detection_method",
            "confidence",
            "description",
        }

        for alert in alerts:
            self.assertTrue(required_fields.issubset(alert.keys()))

    def test_review_alert_records_follow_up_in_review_history(self) -> None:
        alert_id = self.service.get_alerts()[0]["alert_id"]

        review = self.service.review_alert(
            alert_id=alert_id,
            disposition="Needs investigation",
            reason="The sample event needs a second review.",
            reviewer="Terry Li",
            next_action="Compare with related sample logs.",
            owner="Frontend reviewer",
        )

        self.assertEqual(review["alert_id"], alert_id)
        self.assertEqual(review["status"], "Open")
        self.assertEqual(review["data_source"], "Mock/Synthetic")
        self.assertTrue(review["reviewed_at"])
        self.assertEqual(self.service.get_alert_reviews(), [review])

    def test_false_positive_review_record_is_closed_without_follow_up(self) -> None:
        alert_id = self.service.get_alerts()[0]["alert_id"]

        review = self.service.review_alert(
            alert_id=alert_id,
            disposition="False positive",
            reason="This fixture is used as a false-positive exercise.",
            reviewer="Terry Li",
        )

        self.assertEqual(review["status"], "Closed")
        self.assertEqual(review["next_action"], "")
        self.assertEqual(review["owner"], "")

    def test_review_is_a_mock_audit_record_and_does_not_change_alert_state(self) -> None:
        alerts_before = self.service.get_alerts()
        summary_before = self.service.get_dashboard_summary()
        alert_id = alerts_before[0]["alert_id"]

        review = self.service.review_alert(
            alert_id=alert_id,
            disposition="Confirmed incident",
            reason="Synthetic alert retained for investigation.",
            reviewer="Test reviewer",
            next_action="Inspect related mock logs.",
            owner="Test owner",
        )

        timestamp = datetime.fromisoformat(review["reviewed_at"])
        self.assertEqual(timestamp.utcoffset(), timezone.utc.utcoffset(timestamp))
        self.assertEqual(review["status"], "Open")
        self.assertEqual(review["data_source"], "Mock/Synthetic")
        self.assertEqual(self.service.get_alerts(), alerts_before)
        self.assertEqual(self.service.get_dashboard_summary(), summary_before)

    def test_review_alert_rejects_missing_required_review_information(self) -> None:
        alert_id = self.service.get_alerts()[0]["alert_id"]
        invalid_reviews = (
            {"reason": "   ", "reviewer": "Terry Li"},
            {"reason": "Needs follow-up.", "reviewer": "Terry Li"},
            {
                "reason": "Needs follow-up.",
                "reviewer": "Terry Li",
                "next_action": "Review logs.",
            },
        )

        for fields in invalid_reviews:
            with self.subTest(fields=fields):
                with self.assertRaises(ValueError):
                    self.service.review_alert(
                        alert_id=alert_id,
                        disposition="Needs investigation",
                        **fields,
                    )

        self.assertEqual(self.service.get_alert_reviews(), [])

    def test_review_alert_rejects_unknown_alert_and_disposition(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown alert ID"):
            self.service.review_alert(
                "ALT-UNKNOWN", "False positive", "Reason", "Terry Li"
            )

        alert_id = self.service.get_alerts()[0]["alert_id"]
        with self.assertRaisesRegex(ValueError, "unsupported alert disposition"):
            self.service.review_alert(
                alert_id, "Ignore", "Reason", "Terry Li"
            )

    def test_alert_review_history_returns_defensive_copies(self) -> None:
        alert_id = self.service.get_alerts()[0]["alert_id"]
        self.service.review_alert(
            alert_id,
            "False positive",
            "Synthetic exercise.",
            "Terry Li",
        )

        reviews = self.service.get_alert_reviews()
        reviews[0]["reason"] = "Changed outside the service"

        self.assertEqual(
            self.service.get_alert_reviews()[0]["reason"], "Synthetic exercise."
        )

    def test_exported_review_history_is_labeled_and_contains_review_records(self) -> None:
        alert_id = self.service.get_alerts()[0]["alert_id"]
        review = self.service.review_alert(
            alert_id,
            "Needs investigation",
            "Synthetic alert needs a follow-up check.",
            "Test reviewer",
            next_action="Compare related logs.",
            owner="Test owner",
        )

        with workspace_temporary_directory() as temporary_directory:
            destination = Path(temporary_directory) / "review-evidence.json"
            returned_path = self.service.export_alert_reviews(destination)
            exported = json.loads(destination.read_text(encoding="utf-8"))

        timestamp = datetime.fromisoformat(exported["exported_at"])
        self.assertEqual(returned_path, destination)
        self.assertEqual(timestamp.utcoffset(), timezone.utc.utcoffset(timestamp))
        self.assertEqual(exported["data_source"], "Mock/Synthetic")
        self.assertIn("not tamper-resistant", exported["persistence_note"])
        self.assertEqual(exported["reviews"], [review])

    def test_alert_severity_values_are_supported(self) -> None:
        supported_severities = {"Normal", "Low", "Medium", "High"}

        for alert in self.service.get_alerts():
            self.assertIn(alert["severity"], supported_severities)

    def test_alert_confidence_values_are_numeric_and_in_range(self) -> None:
        for alert in self.service.get_alerts():
            confidence = alert["confidence"]
            self.assertIsInstance(confidence, (int, float))
            self.assertGreaterEqual(confidence, 0)
            self.assertLessEqual(confidence, 1)

    def test_block_and_unblock_are_mock_only_and_update_state(self) -> None:
        ip_address = "203.0.113.99"
        block_result = self.service.block_ip(ip_address)
        self.assertTrue(block_result["success"])
        self.assertIn(ip_address, {item["ip_address"] for item in self.service.get_banned_ips()})

        unblock_result = self.service.unblock_ip(ip_address)
        self.assertTrue(unblock_result["success"])
        self.assertNotIn(ip_address, {item["ip_address"] for item in self.service.get_banned_ips()})

    def test_mock_block_rejects_blank_and_duplicate_ips(self) -> None:
        initial_banned_ips = self.service.get_banned_ips()

        blank_result = self.service.block_ip("   ")
        self.assertFalse(blank_result["success"])
        self.assertEqual(self.service.get_banned_ips(), initial_banned_ips)

        existing_ip = initial_banned_ips[0]["ip_address"]
        duplicate_result = self.service.block_ip(existing_ip)
        self.assertFalse(duplicate_result["success"])
        self.assertEqual(self.service.get_banned_ips(), initial_banned_ips)

    def test_unblock_unknown_ip_fails_without_changing_state(self) -> None:
        initial_banned_ips = self.service.get_banned_ips()

        result = self.service.unblock_ip("203.0.113.200")

        self.assertFalse(result["success"])
        self.assertEqual(self.service.get_banned_ips(), initial_banned_ips)

    def test_dashboard_summary_matches_mock_state(self) -> None:
        summary = self.service.get_dashboard_summary()
        self.assertEqual(summary["active_alert_count"], len(self.service.get_alerts()))
        self.assertEqual(summary["banned_ip_count"], len(self.service.get_banned_ips()))

    def test_dashboard_summary_severity_counts_match_alerts(self) -> None:
        summary = self.service.get_dashboard_summary()
        expected_counts = Counter(alert["severity"] for alert in self.service.get_alerts())

        for severity in ("Normal", "Low", "Medium", "High"):
            self.assertEqual(summary["severity_counts"][severity], expected_counts.get(severity, 0))

    def test_getters_return_defensive_copies(self) -> None:
        alerts = self.service.get_alerts()
        alerts[0]["severity"] = "Changed"
        self.assertNotEqual(self.service.get_alerts()[0]["severity"], "Changed")

        banned_ips = self.service.get_banned_ips()
        banned_ips[0]["ip_address"] = "203.0.113.250"
        self.assertNotEqual(self.service.get_banned_ips()[0]["ip_address"], "203.0.113.250")

    def test_get_logs_matches_alert_data_and_expected_shape(self) -> None:
        alerts = self.service.get_alerts()
        logs = self.service.get_logs()
        required_fields = {
            "timestamp",
            "event_type",
            "ip_address",
            "description",
            "severity",
            "action_taken",
        }

        self.assertEqual(len(logs), len(alerts))
        for alert, log in zip(alerts, logs):
            self.assertTrue(required_fields.issubset(log.keys()))
            self.assertEqual(log["timestamp"], alert["timestamp"])
            self.assertEqual(log["ip_address"], alert["source_ip"])
            self.assertEqual(log["description"], alert["description"])
            self.assertEqual(log["severity"], alert["severity"])
            self.assertEqual(log["event_type"], "Security Alert")
            self.assertEqual(log["action_taken"], "Pending review")

    def test_get_settings_returns_expected_shape_and_defensive_copy(self) -> None:
        settings = self.service.get_settings()
        required_fields = {
            "alerts_enabled",
            "logging_enabled",
            "network_interface",
        }

        self.assertTrue(required_fields.issubset(settings.keys()))
        self.assertIsInstance(settings["alerts_enabled"], bool)
        self.assertIsInstance(settings["logging_enabled"], bool)
        self.assertIsInstance(settings["network_interface"], str)

        original_network_interface = settings["network_interface"]
        settings["network_interface"] = "Changed Interface"
        self.assertEqual(
            self.service.get_settings()["network_interface"],
            original_network_interface,
        )

    def test_rejects_alert_file_with_non_list_top_level(self) -> None:
        with workspace_temporary_directory() as temporary_directory:
            data_path = Path(temporary_directory) / "alerts.json"
            data_path.write_text(json.dumps({"alerts": []}), encoding="utf-8")

            with self.assertRaises(ValueError):
                MockIDSService(data_path)

    def test_empty_alert_file_produces_empty_frontend_state(self) -> None:
        with workspace_temporary_directory() as temporary_directory:
            data_path = Path(temporary_directory) / "alerts.json"
            data_path.write_text("[]", encoding="utf-8")

            service = MockIDSService(data_path)

            self.assertEqual(service.get_alerts(), [])
            self.assertEqual(service.get_logs(), [])
            self.assertEqual(service.get_dashboard_summary()["active_alert_count"], 0)
            self.assertEqual(
                service.get_dashboard_summary()["severity_counts"],
                {"Normal": 0, "Low": 0, "Medium": 0, "High": 0},
            )

    def test_rejects_malformed_alert_json(self) -> None:
        with workspace_temporary_directory() as temporary_directory:
            data_path = Path(temporary_directory) / "alerts.json"
            data_path.write_text('[{"alert_id": "A-1"}', encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                MockIDSService(data_path)

    def test_rejects_alert_entries_missing_required_fields(self) -> None:
        with workspace_temporary_directory() as temporary_directory:
            data_path = Path(temporary_directory) / "alerts.json"
            data_path.write_text(json.dumps([{"alert_id": "A-1"}]), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "missing required fields"):
                MockIDSService(data_path)

    def test_rejects_invalid_alert_severity_and_confidence(self) -> None:
        valid_alert = self.service.get_alerts()[0]
        invalid_values = (
            ("severity", "Critical", "unsupported severity"),
            ("confidence", 1.01, "confidence must be a number between 0 and 1"),
            ("confidence", True, "confidence must be a number between 0 and 1"),
        )

        with workspace_temporary_directory() as temporary_directory:
            data_path = Path(temporary_directory) / "alerts.json"

            for field, value, expected_message in invalid_values:
                with self.subTest(field=field, value=value):
                    alert = valid_alert.copy()
                    alert[field] = value
                    data_path.write_text(json.dumps([alert]), encoding="utf-8")

                    with self.assertRaisesRegex(ValueError, expected_message):
                        MockIDSService(data_path)


if __name__ == "__main__":
    unittest.main()
