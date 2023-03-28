"""Class defining the /bots API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Bots(APIEndpoint):
    """Class defining the /bots API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/bots"

    def create_bot(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, options=options)

    def get_bots(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(self.endpoint, params=params)

    def patch_bot(
        self, bot_id: str, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{bot_id}", options=options)

    def get_bot(
        self, bot_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{bot_id}", params=params)

    def disable_bot(self, bot_id: str) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{bot_id}/disable")

    def enable_bot(self, bot_id: str) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{bot_id}/enable")

    def assign_bot_to_user(
        self, bot_id: str, user_id: str
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{bot_id}/assign/{user_id}")

    def get_bot_lhs_icon(
        self, bot_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{bot_id}/icon")

    def set_bot_lhs_icon(
        self, bot_id: str, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{bot_id}/icon", files=files)

    def delete_bot_lhs_icon(self, bot_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/{bot_id}/icon")
