"""Blog service plugin."""

from __future__ import annotations

from typing import Dict, List

from backend.hub.config import ServiceConfig
from backend.hub.registry import ServiceRegistry
from backend.hub.rpc import RpcBus, RpcServer


class Plugin:
    """Blog module demonstrating CRUD-like RPC endpoints."""

    name = "blog"

    def __init__(self, config: ServiceConfig, bus: RpcBus):
        self._config = config
        self._server = RpcServer(bus, self.name)
        self._posts: List[Dict[str, str]] = [
            {
                "id": "1",
                "title": "Hello Hub",
                "body": "This is the first post served through the modular hub.",
            }
        ]
        self._register_routes()

    def _register_routes(self) -> None:
        self._server.register("list", self._list_posts)
        self._server.register("create", self._create_post)

    async def _list_posts(self, payload: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
        return {"posts": self._posts}

    async def _create_post(self, payload: Dict[str, str]) -> Dict[str, str]:
        post = {
            "id": str(len(self._posts) + 1),
            "title": payload.get("title", "Untitled"),
            "body": payload.get("body", ""),
        }
        self._posts.append(post)
        return post

    def register(self, registry: ServiceRegistry) -> None:
        # Nothing to do: the hub owns the registry lifecycle.
        return None

    def get_routes(self) -> dict:
        return {
            "list": self._list_posts,
            "create": self._create_post,
        }
