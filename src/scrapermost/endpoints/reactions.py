"""Endpoints for creating, getting and removing emoji reactions."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .posts import Posts
from .users import Users


@dataclass
class Reactions(APIEndpoint):
    """Class defining the /reactions API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/reactions"

    def create_reaction(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, body_json=body_json)

    def get_reactions_of_post(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{Posts.endpoint}/{post_id}/{self.endpoint}")

    def delete_reaction(
        self,
        user_id: str,
        post_id: str,
        emoji_name: str,
        params: Dict[str, Any] | None = None,
    ) -> Any | Awaitable[Any]:
        return self.client.delete(
            f"{Users.endpoint}/{user_id}/posts/{post_id}/reactions/"
            f"{emoji_name}",
            params=params,
        )
