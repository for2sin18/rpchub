"""Service registry that keeps the hub loosely coupled."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional


@dataclass
class ServiceMetadata:
    """Describe a service registered inside the hub."""

    name: str
    module: str
    config: Dict[str, Any]
    permissions: Iterable[str] = field(default_factory=list)


class ServiceRegistry:
    """In-memory registry with a tiny API surface."""

    def __init__(self) -> None:
        self._services: Dict[str, ServiceMetadata] = {}

    def register(self, metadata: ServiceMetadata) -> None:
        self._services[metadata.name] = metadata

    def unregister(self, name: str) -> None:
        self._services.pop(name, None)

    def get(self, name: str) -> Optional[ServiceMetadata]:
        return self._services.get(name)

    def list(self) -> Dict[str, ServiceMetadata]:
        return dict(self._services)

    def has_permission(self, name: str, role: str) -> bool:
        metadata = self.get(name)
        if not metadata:
            return False
        if not metadata.permissions:
            return True
        return role in set(metadata.permissions)
