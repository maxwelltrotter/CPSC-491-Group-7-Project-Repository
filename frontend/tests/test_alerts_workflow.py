"""Headless regression tests for the Alerts screen's review handlers."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from frontend.alerts import AlertsFrame
from frontend.services.mock_ids_service import MockIDSService


class FakeVar:
    def __init__(self, value: str = "") -> None:
        self.value = value

    def get(self) -> str:
        return self.value

    def set(self, value: str) -> None:
        self.value = value


class FakeTree:
    def __init__(self) -> None:
        self.selected: tuple[str, ...] = ()
        self.rows: dict[str, tuple[str, ...]] = {}

    def selection(self) -> tuple[str, ...]:
        return self.selected

    def get_children(self) -> tuple[str, ...]:
        return tuple(self.rows)

    def delete(self, item: str) -> None:
        del self.rows[item]

    def insert(self, _parent: str, _position: str, *, iid: str, values: tuple) -> None:
        self.rows[iid] = values


def review_screen() -> SimpleNamespace:
    service = MockIDSService()
    state = SimpleNamespace(
        service=service,
        tree=FakeTree(),
        review_tree=FakeTree(),
        selected_alert_var=FakeVar("No alert selected"),
        disposition_var=FakeVar("Needs investigation"),
        reviewer_var=FakeVar("Terry Li"),
        reason_var=FakeVar("Investigate the synthetic connection pattern."),
        next_action_var=FakeVar("Compare related sample logs."),
        owner_var=FakeVar("On-call analyst"),
        review_status_var=FakeVar("Mock/Synthetic review data only"),
    )
    state._refresh_review_history = lambda: AlertsFrame._refresh_review_history(state)
    return state


def test_selecting_and_clearing_alert_updates_selected_id() -> None:
    state = review_screen()
    alert_id = state.service.get_alerts()[0]["alert_id"]

    state.tree.selected = (alert_id,)
    AlertsFrame._on_alert_selected(state, None)
    assert state.selected_alert_var.get() == alert_id

    state.tree.selected = ()
    AlertsFrame._on_alert_selected(state, None)
    assert state.selected_alert_var.get() == "No alert selected"


def test_saving_without_selected_alert_reports_failure_and_preserves_history() -> None:
    state = review_screen()

    with patch("frontend.alerts.messagebox.showerror") as showerror:
        AlertsFrame._save_review(state)

    assert state.review_status_var.get() == "Review not saved"
    assert state.service.get_alert_reviews() == []
    assert state.review_tree.rows == {}
    showerror.assert_called_once()
    assert "Select an alert" in showerror.call_args.args[1]


@pytest.mark.parametrize(
    ("field", "message"),
    (
        ("reason_var", "review reason is required"),
        ("reviewer_var", "reviewer is required"),
        ("next_action_var", "next action is required"),
        ("owner_var", "follow-up owner is required"),
    ),
)
def test_invalid_form_reports_error_without_losing_input(
    field: str, message: str
) -> None:
    state = review_screen()
    state.tree.selected = (state.service.get_alerts()[0]["alert_id"],)
    getattr(state, field).set("   ")
    original_values = tuple(
        var.get()
        for var in (
            state.disposition_var,
            state.reviewer_var,
            state.reason_var,
            state.next_action_var,
            state.owner_var,
        )
    )

    with patch("frontend.alerts.messagebox.showerror") as showerror:
        AlertsFrame._save_review(state)

    assert state.review_status_var.get() == "Review not saved"
    assert state.service.get_alert_reviews() == []
    assert state.review_tree.rows == {}
    assert original_values == tuple(
        var.get()
        for var in (
            state.disposition_var,
            state.reviewer_var,
            state.reason_var,
            state.next_action_var,
            state.owner_var,
        )
    )
    showerror.assert_called_once()
    assert message in showerror.call_args.args[1]


def test_valid_review_refreshes_history_and_clears_follow_up_fields() -> None:
    state = review_screen()
    alert_id = state.service.get_alerts()[0]["alert_id"]
    state.tree.selected = (alert_id,)

    with patch("frontend.alerts.messagebox.showerror") as showerror:
        AlertsFrame._save_review(state)

    review = state.service.get_alert_reviews()[0]
    row = state.review_tree.rows["review-0"]
    assert len(state.service.get_alert_reviews()) == 1
    assert row[:4] == (alert_id, "Needs investigation", "Open", "Terry Li")
    assert row[4] == review["reviewed_at"]
    assert datetime.fromisoformat(row[4]).utcoffset() == timedelta(0)
    assert state.review_status_var.get() == "Mock/Synthetic review saved in memory only"
    assert state.disposition_var.get() == ""
    assert state.reason_var.get() == ""
    assert state.next_action_var.get() == ""
    assert state.owner_var.get() == ""
    assert state.reviewer_var.get() == "Terry Li"
    showerror.assert_not_called()


def test_export_with_no_reviews_skips_file_dialog() -> None:
    state = review_screen()
    state.review_status_var.set("Mock/Synthetic review evidence exported: previous.json")

    with patch("frontend.alerts.filedialog.asksaveasfilename") as save_dialog:
        AlertsFrame._export_review_history(state)

    save_dialog.assert_not_called()
    assert state.review_status_var.get() == "There are no review records to export"
    assert state.service.get_alert_reviews() == []


def test_cancelling_export_does_not_leave_a_stale_success_message() -> None:
    state = review_screen()
    alert_id = state.service.get_alerts()[0]["alert_id"]
    state.service.review_alert(alert_id, "False positive", "Synthetic exercise.", "Terry Li")
    reviews_before = state.service.get_alert_reviews()
    state.review_status_var.set("Mock/Synthetic review evidence exported: previous.json")

    with patch("frontend.alerts.filedialog.asksaveasfilename", return_value=""), patch.object(
        state.service, "export_alert_reviews"
    ) as export:
        AlertsFrame._export_review_history(state)

    export.assert_not_called()
    assert state.review_status_var.get() == "Review history export cancelled"
    assert state.service.get_alert_reviews() == reviews_before


def test_export_write_failure_reports_error_without_changing_history() -> None:
    state = review_screen()
    alert_id = state.service.get_alerts()[0]["alert_id"]
    state.service.review_alert(alert_id, "False positive", "Synthetic exercise.", "Terry Li")
    reviews_before = state.service.get_alert_reviews()
    state.review_status_var.set("Mock/Synthetic review evidence exported: previous.json")

    with patch(
        "frontend.alerts.filedialog.asksaveasfilename", return_value="unwritable.json"
    ), patch.object(state.service, "export_alert_reviews", side_effect=OSError("disk full")), patch(
        "frontend.alerts.messagebox.showerror"
    ) as showerror:
        AlertsFrame._export_review_history(state)

    assert state.review_status_var.get() == "Review history export failed"
    assert state.service.get_alert_reviews() == reviews_before
    showerror.assert_called_once()
    assert "disk full" in showerror.call_args.args[1]


def test_export_multiple_reviews_matches_history_and_is_labeled() -> None:
    state = review_screen()
    alert_ids = [alert["alert_id"] for alert in state.service.get_alerts()]
    state.service.review_alert(alert_ids[0], "False positive", "Known sample.", "Terry Li")
    state.service.review_alert(
        alert_ids[1],
        "Needs investigation",
        "Review this sample.",
        "Terry Li",
        next_action="Compare sample logs.",
        owner="On-call analyst",
    )
    reviews_before = state.service.get_alert_reviews()
    with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2]) as directory:
        destination = Path(directory) / "review-history.json"
        with patch(
            "frontend.alerts.filedialog.asksaveasfilename", return_value=str(destination)
        ):
            AlertsFrame._export_review_history(state)
        exported = json.loads(destination.read_text(encoding="utf-8"))
        assert state.review_status_var.get() == (
            f"Mock/Synthetic review evidence exported: {destination}"
        )
    assert exported["reviews"] == reviews_before
    assert len(exported["reviews"]) == 2
    assert exported["data_source"] == "Mock/Synthetic"
    assert "not tamper-resistant" in exported["persistence_note"]
    assert datetime.fromisoformat(exported["exported_at"]).utcoffset() == timedelta(0)
    assert state.service.get_alert_reviews() == reviews_before
