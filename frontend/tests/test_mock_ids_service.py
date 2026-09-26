from __future__ import annotations

import unittest
from collections import Counter

from frontend.services.mock_ids_service import MockIDSService


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

    def test_alert_severity_values_are_supported(self) -> None:
        supported_severities = {"Normal", "Low", "Medium", "High"}

        for alert in self.service.get_alerts():
            self.assertIn(alert["severity"], supported_severities)

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

    def test_dashboard_summary_matches_mock_state(self) -> None:
        summary = self.service.get_dashboard_summary()
        self.assertEqual(summary["active_alert_count"], len(self.service.get_alerts()))
        self.assertEqual(summary["banned_ip_count"], len(self.service.get_banned_ips()))

    def test_dashboard_summary_severity_counts_match_alerts(self) -> None:
        summary = self.service.get_dashboard_summary()
        expected_counts = Counter(alert["severity"] for alert in self.service.get_alerts())

        for severity in ("Normal", "Low", "Medium", "High"):
            self.assertEqual(summary["severity_counts"][severity], expected_counts.get(severity, 0))


if __name__ == "__main__":
    unittest.main()
