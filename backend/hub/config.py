"""Configuration helpers for the hub platform."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml


@dataclass
class ServiceConfig:
    """In-memory representation of a service entry.

    Attributes
    ----------
    name:
        Unique identifier for the service inside the hub.
    module:
        Dotted path to the Python module implementing the service plugin.
    config:
        Arbitrary configuration payload forwarded to the service plugin.
    permissions:
        Optional list of permission groups allowed to access the service.
    """

    name: str
    module: str
    config: Dict[str, Any]

    @property
    def permissions(self) -> Iterable[str]:
        return self.config.get("permissions", [])


class HubConfig:
    """Load and expose hub settings in a linux-ish, minimalist manner."""

    def __init__(self, service_configs: List[ServiceConfig]):
        self._services = {service.name: service for service in service_configs}

    @classmethod
    def from_path(cls, path: Path) -> "HubConfig":
        data = yaml.safe_load(path.read_text())
        services = [
            ServiceConfig(
                name=item["name"],
                module=item["module"],
                config=item.get("config", {}),
            )
            for item in data.get("services", [])
        ]
        return cls(services)

    def list_services(self) -> List[ServiceConfig]:
        return list(self._services.values())

    def get_service(self, name: str) -> ServiceConfig:
        return self._services[name]


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "services.yaml"


def load_default_config() -> HubConfig:
    """Load the default hub configuration file."""

    return HubConfig.from_path(DEFAULT_CONFIG_PATH)
