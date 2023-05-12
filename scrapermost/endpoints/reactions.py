"""Endpoints for creating, getting and removing emoji reactions."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json
from .posts import Posts
from .users import Users


@dataclass
class Reactions(APIEndpoint):
    """Class defining the Emoji reactions API endpoint.

    Attributes
    ----------
    endpoint : str, default='reactions'
        The endpoint path.

    Methods
    -------
    create_reaction(body_json)
        Create a reaction.
    get_reactions_of_post(post_id)
        Get a list of reactions made by all users to a given post.
    delete_reaction(user_id, post_id, emoji_name)
        Delete a reaction made by a user from the given post.

    """

    endpoint: str = "reactions"

    @_ret_json
    def create_reaction(
        self, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Create a reaction.

        Parameters
        ----------
        body_json : dict
            The reaction settings as a dict.
            Example:
            {
                "user_id": "string",
                "post_id": "string",
                "emoji_name": "string",
                "create_at": 0
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(self.endpoint, body_json=body_json)

    @_ret_json
    def get_reactions_of_post(
        self, post_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of reactions made by all users to a given post.

        Parameters
        ----------
        post_id : str
            Post GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{Posts.endpoint}/{post_id}/{self.endpoint}")

    @_ret_json
    def delete_reaction(
        self,
        user_id: str,
        post_id: str,
        emoji_name: str,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Delete a reaction made by a user from the given post.

        Parameters
        ----------
        user_id : str
            User GUID.
        post_id : str
            Post GUID.
        emoji_name : str
            Emoji name.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete(
            f"{Users.endpoint}/{user_id}/posts/{post_id}/{self.endpoint}/"
            f"{emoji_name}",
        )
