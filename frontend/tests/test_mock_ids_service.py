from __future__ import annotations

import unittest

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
            "description",
        }
        self.assertTrue(required_fields.issubset(alerts[0].keys()))

    def test_block_and_unblock_are_mock_only_and_update_state(self) -> None:
        ip_address = "203.0.113.99"
        block_result = self.service.block_ip(ip_address)
        self.assertTrue(block_result["success"])
        self.assertIn(ip_address, {item["ip_address"] for item in self.service.get_banned_ips()})

        unblock_result = self.service.unblock_ip(ip_address)
        self.assertTrue(unblock_result["success"])
        self.assertNotIn(ip_address, {item["ip_address"] for item in self.service.get_banned_ips()})

    def test_dashboard_summary_matches_mock_state(self) -> None:
        summary = self.service.get_dashboard_summary()
        self.assertEqual(summary["active_alert_count"], len(self.service.get_alerts()))
        self.assertEqual(summary["banned_ip_count"], len(self.service.get_banned_ips()))


if __name__ == "__main__":
    unittest.main()
