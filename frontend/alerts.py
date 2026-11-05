from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .services.ids_service import IDSService


class AlertsFrame(ttk.Frame):
    _REVIEW_DISPOSITIONS = (
        "Confirmed incident",
        "False positive",
        "Needs investigation",
    )

    def __init__(self, parent: tk.Misc, service: IDSService) -> None:
        super().__init__(parent, padding=16)
        self.service = service
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text="Alerts", font=("TkDefaultFont", 18, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = ("timestamp", "source_ip", "threat_type", "severity", "confidence")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        for column, heading in (
            ("timestamp", "Timestamp"),
            ("source_ip", "Source IP"),
            ("threat_type", "Threat Type"),
            ("severity", "Severity"),
            ("confidence", "Confidence"),
        ):
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=140, anchor="w")
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_alert_selected)

        review_frame = ttk.LabelFrame(self, text="Review selected alert", padding=10)
        review_frame.grid(row=2, column=0, sticky="ew", pady=(10, 6))
        review_frame.columnconfigure(1, weight=1)
        review_frame.columnconfigure(3, weight=1)

        self.selected_alert_var = tk.StringVar(value="No alert selected")
        ttk.Label(review_frame, text="Selected alert:").grid(
            row=0, column=0, sticky="w", padx=(0, 6), pady=3
        )
        ttk.Label(review_frame, textvariable=self.selected_alert_var).grid(
            row=0, column=1, columnspan=3, sticky="w", pady=3
        )

        self.disposition_var = tk.StringVar()
        ttk.Label(review_frame, text="Disposition:").grid(
            row=1, column=0, sticky="w", padx=(0, 6), pady=3
        )
        self.disposition_box = ttk.Combobox(
            review_frame,
            textvariable=self.disposition_var,
            values=self._REVIEW_DISPOSITIONS,
            state="readonly",
        )
        self.disposition_box.grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=3)

        self.reviewer_var = tk.StringVar()
        ttk.Label(review_frame, text="Reviewer:").grid(
            row=1, column=2, sticky="w", padx=(0, 6), pady=3
        )
        ttk.Entry(review_frame, textvariable=self.reviewer_var).grid(
            row=1, column=3, sticky="ew", pady=3
        )

        self.reason_var = tk.StringVar()
        ttk.Label(review_frame, text="Reason:").grid(
            row=2, column=0, sticky="w", padx=(0, 6), pady=3
        )
        ttk.Entry(review_frame, textvariable=self.reason_var).grid(
            row=2, column=1, columnspan=3, sticky="ew", pady=3
        )

        self.next_action_var = tk.StringVar()
        ttk.Label(review_frame, text="Next action:").grid(
            row=3, column=0, sticky="w", padx=(0, 6), pady=3
        )
        ttk.Entry(review_frame, textvariable=self.next_action_var).grid(
            row=3, column=1, sticky="ew", padx=(0, 12), pady=3
        )

        self.owner_var = tk.StringVar()
        ttk.Label(review_frame, text="Follow-up owner:").grid(
            row=3, column=2, sticky="w", padx=(0, 6), pady=3
        )
        ttk.Entry(review_frame, textvariable=self.owner_var).grid(
            row=3, column=3, sticky="ew", pady=3
        )

        self.review_status_var = tk.StringVar(value="Mock/Synthetic review data only")
        ttk.Button(review_frame, text="Save review", command=self._save_review).grid(
            row=4, column=2, sticky="e", padx=(0, 8), pady=(6, 0)
        )
        ttk.Button(
            review_frame, text="Export review history", command=self._export_review_history
        ).grid(row=4, column=3, sticky="e", pady=(6, 0))
        ttk.Label(review_frame, textvariable=self.review_status_var).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(6, 0)
        )

        history_frame = ttk.LabelFrame(self, text="Review history", padding=6)
        history_frame.grid(row=3, column=0, sticky="nsew", pady=(4, 0))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        review_columns = ("alert_id", "disposition", "status", "reviewer", "reviewed_at")
        self.review_tree = ttk.Treeview(
            history_frame, columns=review_columns, show="headings", height=4
        )
        for column, heading, width in (
            ("alert_id", "Alert ID", 100),
            ("disposition", "Disposition", 150),
            ("status", "Review Status", 100),
            ("reviewer", "Reviewer", 120),
            ("reviewed_at", "Reviewed At (UTC)", 210),
        ):
            self.review_tree.heading(column, text=heading)
            self.review_tree.column(column, width=width, anchor="w")
        self.review_tree.grid(row=0, column=0, sticky="nsew")

        self.refresh()

    def refresh(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for alert in self.service.get_alerts():
            confidence = alert.get("confidence")
            confidence_text = "" if confidence is None else f"{float(confidence):.0%}"
            self.tree.insert(
                "",
                "end",
                iid=str(alert.get("alert_id", "")),
                values=(
                    alert.get("timestamp", ""),
                    alert.get("source_ip", ""),
                    alert.get("threat_type", ""),
                    alert.get("severity", ""),
                    confidence_text,
                ),
            )
        self._refresh_review_history()

    def _on_alert_selected(self, _event: tk.Event[tk.Misc]) -> None:
        selected = self.tree.selection()
        self.selected_alert_var.set(selected[0] if selected else "No alert selected")

    def _refresh_review_history(self) -> None:
        for item in self.review_tree.get_children():
            self.review_tree.delete(item)
        for index, review in enumerate(self.service.get_alert_reviews()):
            self.review_tree.insert(
                "",
                "end",
                iid=f"review-{index}",
                values=(
                    review.get("alert_id", ""),
                    review.get("disposition", ""),
                    review.get("status", ""),
                    review.get("reviewer", ""),
                    review.get("reviewed_at", ""),
                ),
            )

    def _save_review(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror(
                "Review not saved", "Select an alert before saving a review.", parent=self
            )
            return

        try:
            self.service.review_alert(
                alert_id=selected[0],
                disposition=self.disposition_var.get(),
                reason=self.reason_var.get(),
                reviewer=self.reviewer_var.get(),
                next_action=self.next_action_var.get(),
                owner=self.owner_var.get(),
            )
        except ValueError as error:
            self.review_status_var.set("Review not saved")
            messagebox.showerror("Review not saved", str(error), parent=self)
            return

        self._refresh_review_history()
        self.review_status_var.set("Mock/Synthetic review saved in memory only")
        self.disposition_var.set("")
        self.reason_var.set("")
        self.next_action_var.set("")
        self.owner_var.set("")

    def _export_review_history(self) -> None:
        reviews = self.service.get_alert_reviews()
        if not reviews:
            self.review_status_var.set("There are no review records to export")
            return

        destination = filedialog.asksaveasfilename(
            parent=self,
            title="Export mock alert review history",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"),),
            initialfile="mock_alert_review_history.json",
        )
        if not destination:
            return

        try:
            export_path = self.service.export_alert_reviews(destination)
        except OSError as error:
            self.review_status_var.set("Review history export failed")
            messagebox.showerror("Export failed", str(error), parent=self)
            return

        self.review_status_var.set(f"Mock/Synthetic review evidence exported: {export_path}")
