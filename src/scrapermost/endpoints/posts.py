"""Endpoints for creating, getting and interacting with posts."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .channels import Channels
from .teams import Teams
from .users import Users


@dataclass
class Posts(APIEndpoint):
    """Class defining the Posts API endpoint.

    Attributes
    ----------
    endpoint : str, default='posts'
        The endpoint path.

    Methods
    -------
    create_post(body_json)
        Create a new post in a channel.
    create_ephemeral_post(body_json)
        Create a new ephemeral post in a channel.
    get_post(post_id)
        Get channel from the provided channel ID string.
    delete_post(post_id)
        Mark the post as deleted in the database.
    update_post(post_id, body_json)
        Update a post.
    patch_post(post_id, body_json)
        Partially update a post by providing only the fields to update.
    get_thread(post_id)
        Get a post and the rest of the posts in the same thread.
    get_list_of_flagged_posts(user_id)
        Get a page of flagged posts of a user provided user ID string.
    get_file_info_for_post(post_id)
        Get a list of information for the files attached to a post.
    get_posts_for_channel(channel_id, params)
        Get a page of posts in a channel.
    get_unread_posts_for_channel(user_id, channel_id, params=None)
        Get posts around oldest unread.
    search_for_team_posts(team_id, body_json)
        Search posts in the team and from the provided terms string.
    pin_post_to_channel(post_id)
        Pin a post to the channel.
    unpin_post_to_channel(post_id)
        Unpin a post to the channel.
    perform_post_action(post_id, action_id)
        Perform a post action.

    """

    endpoint: str = "posts"

    def create_post(self, body_json: Dict[str, Any]) -> Any | Awaitable[Any]:
        """Create a new post in a channel.

        To create the post as a comment on another post, provide root_id.

        Parameters
        ----------
        body_json : dict
            The post content and settings as a dict.
            Example:
            {
                "channel_id": "string",
                "message": "string",
                "root_id": "string",
                "file_ids": [
                    "string"
                ],
                "props": {}
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(self.endpoint, body_json=body_json)

    def create_ephemeral_post(
        self, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Create a new ephemeral post in a channel.

        Parameters
        ----------
        body_json : dict
            The post content and settings as a dict.
            Example:
            {
                "user_id": "string",
                "post": {
                    "channel_id": "string",
                    "message": "string"
                }
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/ephemeral", body_json=body_json
        )

    def get_post(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get channel from the provided channel ID string.

        Parameters
        ----------
        post_id : str
            ID of the post to get.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{post_id}")

    def delete_post(self, post_id: str) -> Any | Awaitable[Any]:
        """Mark the post as deleted in the database.

        Parameters
        ----------
        post_id : str
            ID of the post to delete.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(f"{self.endpoint}/{post_id}")

    def update_post(
        self, post_id: str, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Update a post.

        Parameters
        ----------
        post_id : str
            ID of the post to update.
        body_json : dict
            The post content and settings as a dict.
            Example:
            {
                "id": "string",
                "is_pinned": true,
                "message": "string",
                "has_reactions": true,
                "props": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{post_id}", body_json=body_json
        )

    def patch_post(
        self, post_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        """Partially update a post by providing only the fields to update.

        Parameters
        ----------
        post_id : str
            ID of the post to update.
        body_json : dict
            The post content and settings as a dict.
            Example:
            {
                "is_pinned": true,
                "message": "string",
                "file_ids": [
                    "string"
                ],
                "has_reactions": true,
                "props": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{post_id}/patch", body_json=body_json
        )

    def get_thread(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a post and the rest of the posts in the same thread.

        Parameters
        ----------
        post_id : str
            ID of a post in the thread.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/{post_id}/thread",
        )

    def get_list_of_flagged_posts(
        self, user_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of flagged posts of a user provided user ID string.

        Parameters
        ----------
        user_id : str
            User GUID.
        params : dict, optional
            Query parameters to include.
            Example:
            {
                "team_id": "string",
                "channel_id": "string",
                "page": 0,
                "per_page": 60
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Users.endpoint}/{user_id}/{self.endpoint}/flagged",
            params=params,
        )

    def get_file_info_for_post(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of information for the files attached to a post.

        Parameters
        ----------
        post_id : str
            Post GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{post_id}/files/info")

    def get_posts_for_channel(
        self, channel_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of posts in a channel.

        Parameters
        ----------
        channel_id : str
            The channel ID to get the posts for.
        params : dict, optional
            Query parameters to include.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Channels.endpoint}/{channel_id}/{self.endpoint}", params=params
        )

    def get_unread_posts_for_channel(
        self,
        user_id: str,
        channel_id: str,
        params: Dict[str, Any] | None = None,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get posts around oldest unread.

        Parameters
        ----------
        user_id : str
            User GUID.
        channel_id : str
            Channel GUID.
        params : dict, optional
            Query parameters to include.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Users.endpoint}/{user_id}/channels/{channel_id}/posts/unread",
            params=params,
        )

    def search_for_team_posts(
        self, team_id: str, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Search posts in the team and from the provided terms string.

        Parameters
        ----------
        team_id : str
            Team GUID.
        body_json : dict
            The search settings as a dict.
            Example:
            {
                "terms": "string",
                "is_or_search": true,
                "time_zone_offset": 0,
                "include_deleted_channels": true,
                "page": 0,
                "per_page": 60
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{Teams.endpoint}/{team_id}/{self.endpoint}/search",
            body_json=body_json,
        )

    def pin_post_to_channel(self, post_id: str) -> Any | Awaitable[Any]:
        """Pin a post to the channel.

        Parameters
        ----------
        post_id : str
            Post GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/{post_id}/pin")

    def unpin_post_to_channel(self, post_id: str) -> Any | Awaitable[Any]:
        """Unpin a post to the channel.

        Parameters
        ----------
        post_id : str
            Post GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/{post_id}/unpin")

    def perform_post_action(
        self, post_id: str, action_id: str
    ) -> Any | Awaitable[Any]:
        """Perform a post action.

        Parameters
        ----------
        post_id : str
            Post GUID.
        action_id : str
            Action GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{post_id}/actions/{action_id}"
        )
