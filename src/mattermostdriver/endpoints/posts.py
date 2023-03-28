"""Class defining the /posts API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .channels import Channels
from .teams import Teams
from .users import Users


@dataclass
class Posts(APIEndpoint):
    """Class defining the /posts API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/posts"

    def create_post(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, options=options)

    def create_ephemeral_post(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/ephemeral", options=options)

    def get_post(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{post_id}")

    def delete_post(self, post_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/{post_id}")

    def update_post(
        self, post_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(f"{self.endpoint}/{post_id}", options=options)

    def patch_post(
        self, post_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{post_id}/patch", options=options
        )

    def get_thread(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{post_id}/thread",
        )

    def get_list_of_flagged_posts(
        self, user_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/posts/flagged", params=params
        )

    def get_file_info_for_post(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{post_id}/files/info")

    def get_posts_for_channel(
        self, channel_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Channels.endpoint}/{channel_id}/posts", params=params
        )

    def search_for_team_posts(
        self, team_id: str, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{Teams.endpoint}/{team_id}/posts/search", options=options
        )

    def pin_post_to_channel(self, post_id: str) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{post_id}/pin")

    def unpin_post_to_channel(self, post_id: str) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/{post_id}/unpin")

    def perform_post_action(
        self, post_id: str, action_id: str
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/{post_id}/actions/{action_id}"
        )

    def get_unread_posts_for_channel(
        self,
        user_id: str,
        channel_id: str,
        params: Dict[str, Any] | None = None,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/channels/{channel_id}/posts/unread",
            params=params,
        )
