"""Frontend-facing service interfaces and mock implementations."""

from .ids_service import IDSService
from .mock_ids_service import MockIDSService

__all__ = ["IDSService", "MockIDSService"]
