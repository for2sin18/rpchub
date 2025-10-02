"""Simple RPC implementation shared by the hub and services."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict

RpcHandler = Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]


@dataclass
class RpcMessage:
    """Representation of a request in the message bus."""

    service: str
    method: str
    payload: Dict[str, Any]


class RpcBus:
    """Async message bus built on top of :mod:`asyncio`."""

    def __init__(self) -> None:
        self._handlers: Dict[str, RpcHandler] = {}

    def register_handler(self, name: str, handler: RpcHandler) -> None:
        self._handlers[name] = handler

    async def request(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        handler = self._handlers.get(name)
        if handler is None:
            raise RuntimeError(f"No RPC handler registered for {name}")
        return await handler(payload)


class RpcClient:
    """Client used by services to call each other."""

    def __init__(self, bus: RpcBus):
        self._bus = bus

    async def call(self, service: str, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        message = {"service": service, "method": method, "payload": payload}
        return await self._bus.request(service, message)


class RpcServer:
    """Server that exposes service operations."""

    def __init__(self, bus: RpcBus, service_name: str):
        self._bus = bus
        self._service_name = service_name
        self._routes: Dict[str, RpcHandler] = {}
        self._bus.register_handler(service_name, self._dispatch)

    def register(self, method: str, handler: RpcHandler) -> None:
        self._routes[method] = handler

    async def _dispatch(self, message: Dict[str, Any]) -> Dict[str, Any]:
        method = message.get("method")
        payload = message.get("payload", {})
        handler = self._routes.get(method)
        if handler is None:
            raise RuntimeError(f"Method {method} not found for {self._service_name}")
        return await handler(payload)


async def invoke(bus: RpcBus, message: RpcMessage) -> Dict[str, Any]:
    """Helper used by tests or scripts to send messages."""

    client = RpcClient(bus)
    return await client.call(message.service, message.method, message.payload)
