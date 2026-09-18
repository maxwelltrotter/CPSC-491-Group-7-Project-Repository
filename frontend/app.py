from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .alerts import AlertsFrame
from .ban_list import BanListFrame
from .dashboard import DashboardFrame
from .log_history import LogHistoryFrame
from .services.mock_ids_service import MockIDSService
from .settings import SettingsFrame


class AIIDSApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AI-IDS")
        self.geometry("1000x650")
        self.minsize(800, 500)

        self.service = MockIDSService()

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        navigation = ttk.Frame(container, padding=(4, 8))
        navigation.grid(row=0, column=0, sticky="ns")

        self.content = ttk.Frame(container)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.frames = {
            "Dashboard": DashboardFrame(self.content, self.service),
            "Alerts": AlertsFrame(self.content, self.service),
            "Log History": LogHistoryFrame(self.content, self.service),
            "Ban List": BanListFrame(self.content, self.service),
            "Settings": SettingsFrame(self.content, self.service),
        }

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(navigation, text="AI-IDS", font=("TkDefaultFont", 16, "bold")).pack(
            anchor="w", pady=(0, 12)
        )
        for name in self.frames:
            ttk.Button(
                navigation,
                text=name,
                width=18,
                command=lambda page=name: self.show_frame(page),
            ).pack(fill="x", pady=3)

        self.show_frame("Dashboard")

    def show_frame(self, name: str) -> None:
        frame = self.frames[name]
        refresh = getattr(frame, "refresh", None)
        if callable(refresh):
            refresh()
        frame.tkraise()


def run() -> None:
    app = AIIDSApp()
    app.mainloop()
