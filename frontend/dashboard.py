from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .services.ids_service import IDSService


class DashboardFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, service: IDSService) -> None:
        super().__init__(parent, padding=16)
        self.service = service
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Dashboard", font=("TkDefaultFont", 18, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        self.summary_label = ttk.Label(self, justify="left")
        self.summary_label.grid(row=1, column=0, sticky="w")
        self.refresh()

    def refresh(self) -> None:
        summary = self.service.get_dashboard_summary()
        severities = summary.get("severity_counts", {})
        text = (
            f"Devices: {summary.get('device_count', 0)}\n"
            f"Active alerts: {summary.get('active_alert_count', 0)}\n"
            f"Banned IPs: {summary.get('banned_ip_count', 0)}\n\n"
            "Severity summary:\n"
            f"  Normal: {severities.get('Normal', 0)}\n"
            f"  Low: {severities.get('Low', 0)}\n"
            f"  Medium: {severities.get('Medium', 0)}\n"
            f"  High: {severities.get('High', 0)}"
        )
        self.summary_label.configure(text=text)
