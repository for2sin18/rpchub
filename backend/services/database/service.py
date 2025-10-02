"""Database configuration service plugin."""

from __future__ import annotations

from typing import Dict

from backend.hub.config import ServiceConfig
from backend.hub.registry import ServiceRegistry
from backend.hub.rpc import RpcBus, RpcServer


class Plugin:
    """Expose database credentials via RPC in a controlled manner."""

    name = "database"

    def __init__(self, config: ServiceConfig, bus: RpcBus):
        self._config = config
        self._server = RpcServer(bus, self.name)
        self._register_routes()

    def _register_routes(self) -> None:
        self._server.register("dsn", self._get_dsn)

    async def _get_dsn(self, payload: Dict[str, str]) -> Dict[str, str]:
        return {"dsn": self._config.config.get("database_url", "")}

    def register(self, registry: ServiceRegistry) -> None:
        return None

    def get_routes(self) -> dict:
        return {"dsn": self._get_dsn}
