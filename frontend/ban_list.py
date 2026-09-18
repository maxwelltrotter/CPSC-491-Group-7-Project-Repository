from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .services.ids_service import IDSService


class BanListFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, service: IDSService) -> None:
        super().__init__(parent, padding=16)
        self.service = service
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="Ban List", font=("TkDefaultFont", 18, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        controls = ttk.Frame(self)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        controls.columnconfigure(1, weight=1)
        ttk.Label(controls, text="IP Address:").grid(row=0, column=0, padx=(0, 8))
        self.ip_entry = ttk.Entry(controls)
        self.ip_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ttk.Button(controls, text="Mock Block", command=self._block).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(controls, text="Mock Unblock", command=self._unblock).grid(row=0, column=3)

        columns = ("ip_address", "blocked_at", "reason", "severity")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for column, heading in (
            ("ip_address", "IP Address"),
            ("blocked_at", "Blocked At"),
            ("reason", "Reason"),
            ("severity", "Severity"),
        ):
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=170, anchor="w")
        self.tree.grid(row=2, column=0, sticky="nsew")
        self.refresh()

    def _block(self) -> None:
        result = self.service.block_ip(self.ip_entry.get().strip())
        messagebox.showinfo("Mock Response", result["message"])
        self.refresh()

    def _unblock(self) -> None:
        result = self.service.unblock_ip(self.ip_entry.get().strip())
        messagebox.showinfo("Mock Response", result["message"])
        self.refresh()

    def refresh(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for banned in self.service.get_banned_ips():
            self.tree.insert(
                "",
                "end",
                values=(
                    banned.get("ip_address", ""),
                    banned.get("blocked_at", ""),
                    banned.get("reason", ""),
                    banned.get("severity", ""),
                ),
            )
