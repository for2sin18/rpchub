"""Plugin loader used by the hub to bootstrap services."""

from __future__ import annotations

from importlib import import_module
from typing import Protocol

from .config import ServiceConfig
from .registry import ServiceRegistry
from .rpc import RpcBus


class ServicePlugin(Protocol):
    """Interface that service plugins must implement."""

    name: str

    def register(self, registry: ServiceRegistry) -> None:
        ...

    def get_routes(self) -> dict:
        ...


class PluginLoader:
    """Load service plugins based on configuration."""

    def __init__(self, registry: ServiceRegistry, bus: RpcBus):
        self._registry = registry
        self._bus = bus
        self._plugins: dict[str, ServicePlugin] = {}

    def load(self, config: ServiceConfig) -> ServicePlugin:
        module = import_module(config.module)
        plugin: ServicePlugin = module.Plugin(config, self._bus)
        plugin.register(self._registry)
        self._plugins[config.name] = plugin
        return plugin

    def get_plugin(self, name: str) -> ServicePlugin | None:
        return self._plugins.get(name)

    def list_plugins(self) -> dict[str, ServicePlugin]:
        return dict(self._plugins)
