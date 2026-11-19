"""Checks that a teammate can validate the documented mock demo fixture headlessly."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from frontend.demo_preflight import check_demo_data
from frontend.services.mock_ids_service import MockIDSService


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_demo_preflight_accepts_bundled_three_alert_fixture() -> None:
    assert check_demo_data() == {
        "alert_count": 3,
        "alert_ids": ["ALT-001", "ALT-002", "ALT-003"],
    }


def test_demo_preflight_rejects_duplicate_alert_ids() -> None:
    alerts = MockIDSService().get_alerts()
    alerts[1]["alert_id"] = alerts[0]["alert_id"]
    with tempfile.TemporaryDirectory(dir=REPO_ROOT) as directory:
        path = Path(directory) / "alerts.json"
        path.write_text(json.dumps(alerts), encoding="utf-8")
        with pytest.raises(ValueError, match="duplicate IDs"):
            check_demo_data(path)


def test_demo_preflight_rejects_missing_script_alert() -> None:
    alerts = MockIDSService().get_alerts()[:2]
    with tempfile.TemporaryDirectory(dir=REPO_ROOT) as directory:
        path = Path(directory) / "alerts.json"
        path.write_text(json.dumps(alerts), encoding="utf-8")
        with pytest.raises(ValueError, match="ALT-001, ALT-002, and ALT-003"):
            check_demo_data(path)


def test_demo_preflight_command_does_not_open_the_gui() -> None:
    result = subprocess.run(
        [sys.executable, "-B", "-m", "frontend", "--check-demo"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Demo preflight OK: 3 Mock/Synthetic alerts" in result.stdout
    assert "does not verify that a desktop GUI can launch" in result.stdout
