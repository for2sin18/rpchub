"""Minimal authentication helpers."""

from __future__ import annotations

from typing import Dict


class PermissionError(RuntimeError):
    """Raised when a caller is not allowed to access a resource."""


class AuthManager:
    """Mock role mapping kept simple on purpose."""

    def __init__(self, role_tokens: Dict[str, str]):
        self._role_tokens = role_tokens

    def resolve_role(self, token: str) -> str:
        for role, stored_token in self._role_tokens.items():
            if stored_token == token:
                return role
        raise PermissionError("Invalid authentication token")
