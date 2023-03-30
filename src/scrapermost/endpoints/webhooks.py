"""Class defining the /hooks API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Webhooks(APIEndpoint):
    """Class defining the /hooks API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/hooks"

    def create_incoming_hook(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/incoming", options=options)

    def list_incoming_hooks(
        self, params: Dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/incoming", params=params)

    def get_incoming_hook(
        self, hook_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/incoming/{hook_id}")

    def update_incoming_hook(
        self, hook_id: str, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/incoming/{hook_id}", options=options
        )

    def create_outgoing_hook(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/outgoing", options=options)

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
        self, hook_id: str, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/outgoing/{hook_id}", options=options
        )

    def regenerate_token_outgoing_hook(
        self, hook_id: str
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/outgoing/{hook_id}/regen_token"
        )

    def call_webhook(
        self, hook_id: str, options: Dict[str, Any] | None = None
    ) -> Response | Awaitable[Response]:
        return self.client.make_request("post", f"/{hook_id}", options=options)
