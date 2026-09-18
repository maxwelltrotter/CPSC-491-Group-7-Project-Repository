from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .services.ids_service import IDSService


class SettingsFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, service: IDSService) -> None:
        super().__init__(parent, padding=16)
        self.service = service

        ttk.Label(self, text="Settings", font=("TkDefaultFont", 18, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        settings = self.service.get_settings()
        ttk.Label(self, text=f"Alerts enabled: {settings.get('alerts_enabled')}").grid(row=1, column=0, sticky="w")
        ttk.Label(self, text=f"Logging enabled: {settings.get('logging_enabled')}").grid(row=2, column=0, sticky="w")
        ttk.Label(self, text=f"Network interface: {settings.get('network_interface')}").grid(row=3, column=0, sticky="w")
        ttk.Label(
            self,
            text="Settings are mock/read-only during Sprint 1 frontend development.",
        ).grid(row=4, column=0, sticky="w", pady=(12, 0))
