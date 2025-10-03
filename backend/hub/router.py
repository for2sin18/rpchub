"""HTTP routes exposed by the hub platform."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .auth import AuthManager, PermissionError
from .loader import PluginLoader
from .registry import ServiceRegistry
from .rpc import RpcBus, RpcClient


def create_router(
    registry: ServiceRegistry,
    loader: PluginLoader,
    auth: AuthManager,
    bus: RpcBus,
) -> APIRouter:
    router = APIRouter(prefix="/api")
    client = RpcClient(bus)

    @router.get("/services")
    def list_services():
        """Return registered services."""

        return [
            {
                "name": metadata.name,
                "module": metadata.module,
                "config": {k: v for k, v in metadata.config.items() if k != "permissions"},
                "permissions": list(metadata.permissions),
            }
            for metadata in registry.list().values()
        ]

    @router.get("/services/{service_name}")
    def get_service(service_name: str):
        metadata = registry.get(service_name)
        if metadata is None:
            raise HTTPException(status_code=404, detail="Service not found")
        return {
            "name": metadata.name,
            "module": metadata.module,
            "config": {k: v for k, v in metadata.config.items() if k != "permissions"},
            "permissions": list(metadata.permissions),
        }

    @router.post("/services/{service_name}/route/{operation}")
    async def call_service(
        service_name: str, operation: str, token: str, payload: dict
    ):
        try:
            role = auth.resolve_role(token)
        except PermissionError as exc:  # pragma: no cover - trivial branch
            raise HTTPException(status_code=401, detail=str(exc)) from exc

        if not registry.has_permission(service_name, role):
            raise HTTPException(status_code=403, detail="Access denied")

        plugin = loader.get_plugin(service_name)
        if plugin is None:
            raise HTTPException(status_code=404, detail="Service not available")

        try:
            return await client.call(service_name, operation, payload)
        except RuntimeError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return router
