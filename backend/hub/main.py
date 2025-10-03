"""Entrypoint for the hub FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI

from .auth import AuthManager
from .config import HubConfig, load_default_config
from .loader import PluginLoader
from .registry import ServiceMetadata, ServiceRegistry
from .router import create_router
from .rpc import RpcBus


def create_app(config: HubConfig | None = None) -> FastAPI:
    config = config or load_default_config()

    registry = ServiceRegistry()
    bus = RpcBus()
    loader = PluginLoader(registry, bus)
    auth = AuthManager(
        {
            "public": "public-token",
            "editor": "editor-token",
            "admin": "admin-token",
        }
    )

    for service in config.list_services():
        metadata = ServiceMetadata(
            name=service.name,
            module=service.module,
            config=service.config,
            permissions=list(service.permissions),
        )
        registry.register(metadata)
        loader.load(service)

    app = FastAPI(title="Modular RPC Hub")
    app.include_router(create_router(registry, loader, auth, bus))
    return app


app = create_app()
