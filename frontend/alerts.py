from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .services.ids_service import IDSService


class AlertsFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, service: IDSService) -> None:
        super().__init__(parent, padding=16)
        self.service = service
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

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
                values=(
                    alert.get("timestamp", ""),
                    alert.get("source_ip", ""),
                    alert.get("threat_type", ""),
                    alert.get("severity", ""),
                    confidence_text,
                ),
            )
