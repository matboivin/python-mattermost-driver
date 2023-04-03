"""Endpoints for creating, getting and updating webhooks."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Webhooks(APIEndpoint):
    """Class defining the /hooks API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/hooks"

    def create_incoming_hook(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/incoming", body_json=body_json
        )

    def list_incoming_hooks(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/incoming", params=params)

    def get_incoming_hook(
        self, hook_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/incoming/{hook_id}")

    def update_incoming_hook(
        self, hook_id: str, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/incoming/{hook_id}", body_json=body_json
        )

    def create_outgoing_hook(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/outgoing", body_json=body_json
        )

    def list_outgoing_hooks(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/outgoing", params=params)

    def get_outgoing_hook(
        self, hook_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/outgoing/{hook_id}")

    def delete_outgoing_hook(self, hook_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/outgoing/{hook_id}")

    def update_outgoing_hook(
        self, hook_id: str, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/outgoing/{hook_id}", body_json=body_json
        )

    def regenerate_token_outgoing_hook(
        self, hook_id: str
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/outgoing/{hook_id}/regen_token"
        )

    def call_webhook(
        self, hook_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any:
        return self.client.post(
            f"/{hook_id}", body_json=body_json, rec_json=False
        )
