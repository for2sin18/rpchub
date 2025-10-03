"""Comments service demonstrating RPC calls to the blog service."""

from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List

from backend.hub.config import ServiceConfig
from backend.hub.registry import ServiceRegistry
from backend.hub.rpc import RpcBus, RpcClient, RpcServer


class Plugin:
    """Comment module keeping its own state while calling the blog service."""

    name = "comments"

    def __init__(self, config: ServiceConfig, bus: RpcBus):
        self._config = config
        self._bus = bus
        self._server = RpcServer(bus, self.name)
        self._client = RpcClient(bus)
        self._comments: DefaultDict[str, List[Dict[str, str]]] = defaultdict(list)
        self._register_routes()

    def _register_routes(self) -> None:
        self._server.register("list", self._list_comments)
        self._server.register("add", self._add_comment)

    async def _list_comments(self, payload: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
        post_id = payload.get("post_id", "1")
        return {"comments": self._comments[post_id]}

    async def _add_comment(self, payload: Dict[str, str]) -> Dict[str, str]:
        post_id = payload.get("post_id", "1")
        # Validate the post via RPC to keep the modules decoupled.
        await self._client.call("blog", "list", {})
        comment = {
            "author": payload.get("author", "anonymous"),
            "body": payload.get("body", ""),
        }
        self._comments[post_id].append(comment)
        return comment

    def register(self, registry: ServiceRegistry) -> None:
        return None

    def get_routes(self) -> dict:
        return {
            "list": self._list_comments,
            "add": self._add_comment,
        }
