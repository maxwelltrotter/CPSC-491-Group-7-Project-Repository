from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .services.ids_service import IDSService


class LogHistoryFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, service: IDSService) -> None:
        super().__init__(parent, padding=16)
        self.service = service
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Label(self, text="Log History", font=("TkDefaultFont", 18, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        columns = ("timestamp", "event_type", "ip_address", "severity", "action_taken")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        for column, heading in (
            ("timestamp", "Timestamp"),
            ("event_type", "Event Type"),
            ("ip_address", "IP Address"),
            ("severity", "Severity"),
            ("action_taken", "Action"),
        ):
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=140, anchor="w")
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.refresh()

    def refresh(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for log in self.service.get_logs():
            self.tree.insert(
                "",
                "end",
                values=(
                    log.get("timestamp", ""),
                    log.get("event_type", ""),
                    log.get("ip_address", ""),
                    log.get("severity", ""),
                    log.get("action_taken", ""),
                ),
            )
