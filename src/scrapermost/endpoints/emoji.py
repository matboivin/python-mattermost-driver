"""Endpoints for creating, getting and interacting with emojis."""

from dataclasses import dataclass
from json import dumps
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Emoji(APIEndpoint):
    """Class defining the /emoji API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/emoji"

    def create_custom_emoji(
        self, emoji_name: str, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        emoji: Dict[str, Any] = {
            "name": emoji_name,
            "creator_id": self.client.user_id,
        }
        return self.client.post(
            self.endpoint, data={"emoji": dumps(emoji)}, files=files
        )

    def get_emoji_list(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(self.endpoint, params=params)

    def get_custom_emoji(
        self, emoji_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{emoji_id}")

    def delete_custom_emoji(self, emoji_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/{emoji_id}")

    def get_custom_emoji_by_name(
        self, name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/name/{name}")

    def get_custom_emoji_image(
        self, emoji_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{emoji_id}/image")

    def search_custom_emoji(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/search", body_json=body_json)

    def autocomplete_custom_emoji(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/autocomplete", params=params)
