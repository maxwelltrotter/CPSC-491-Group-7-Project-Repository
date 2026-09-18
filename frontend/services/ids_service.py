from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IDSService(ABC):
    """Frontend-facing contract for IDS data and response actions.

    This interface intentionally contains no monitoring, detection, ML, or firewall
    implementation. It only defines what the frontend expects from a service layer.
    """

    @abstractmethod
    def get_dashboard_summary(self) -> dict[str, Any]:
        """Return high-level values for the dashboard."""

    @abstractmethod
    def get_alerts(self) -> list[dict[str, Any]]:
        """Return alert records for presentation."""

    @abstractmethod
    def get_logs(self) -> list[dict[str, Any]]:
        """Return log records for presentation."""

    @abstractmethod
    def get_banned_ips(self) -> list[dict[str, Any]]:
        """Return currently blocked IP records."""

    @abstractmethod
    def block_ip(self, ip_address: str) -> dict[str, Any]:
        """Request that an IP be blocked and return a result payload."""

    @abstractmethod
    def unblock_ip(self, ip_address: str) -> dict[str, Any]:
        """Request that an IP be unblocked and return a result payload."""

    @abstractmethod
    def get_settings(self) -> dict[str, Any]:
        """Return frontend-visible settings."""
