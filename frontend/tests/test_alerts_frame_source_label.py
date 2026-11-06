from __future__ import annotations

import unittest

from frontend.alerts import AlertsFrame


class AlertsFrameSourceLabelTests(unittest.TestCase):
    def test_alert_source_label_distinguishes_mock_from_verified_data(self) -> None:
        self.assertIn("Mock/Synthetic", AlertsFrame._ALERT_SOURCE_LABEL)
        self.assertIn("Backend integration not verified", AlertsFrame._ALERT_SOURCE_LABEL)


if __name__ == "__main__":
    unittest.main()
