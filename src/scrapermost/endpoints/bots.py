"""Endpoints for creating, getting and updating bot users."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Bots(APIEndpoint):
    """Class defining the Bots API endpoint.

    Attributes
    ----------
    endpoint : str, default='bots'
        The endpoint path.

    Methods
    -------
    create_bot(body_json)
        Create a new bot account on the system.
    get_bots(params)
        Get a page of a list of bots.
    patch_bot(bot_id, body_json)
        Update a bot partially by providing only the fields to update.
    get_bot(bot_id, include_deleted)
        Get a bot specified by its bot ID.
    disable_bot(bot_id)
        Disable a bot.
    enable_bot(bot_id)
        Enable a bot.
    assign_bot_to_user(bot_id, user_id)
        Assign a bot to a specified user.
    get_bot_lhs_icon(bot_id)
        Get a bot's Left-Hand Sidebar icon image.
    set_bot_lhs_icon(bot_id, image)
        Set a bot's Left-Hand Sidebar icon image.
    delete_bot_lhs_icon(bot_id)
        Delete a bot's Left-Hand Sidebar icon image.

    """

    endpoint: str = "bots"

    def create_bot(self, body_json: Dict[str, Any]) -> Any | Awaitable[Any]:
        """Create a new bot account on the system.

        Parameters
        ----------
        body_json : dict
            The new bot settings as a dict.
            Example:
            {
                "username": "string",
                "display_name": "string",
                "description": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(self.endpoint, body_json=body_json)

    def get_bots(
        self, params: Dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of a list of bots.

        Parameters
        ----------
        params : dict
            Query parameters to include.
            Example:
            {
                "page": 0,
                "per_page": 0,
                "include_deleted": true,
                "only_orphaned": false
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(self.endpoint, params=params)

    def patch_bot(
        self, bot_id: str, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Update a bot partially by providing only the fields to update.

        Parameters
        ----------
        bot_id : str
            Bot user ID.
        body_json : dict
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{bot_id}", body_json=body_json
        )

    def get_bot(
        self, bot_id: str, include_deleted: bool
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a bot specified by its bot ID.

        Parameters
        ----------
        bot_id : str
            Bot user ID.
        include_deleted : bool
            Whether deleted bots should be returned.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/{bot_id}",
            params={"include_deleted": include_deleted},
        )

    def disable_bot(self, bot_id: str) -> Any | Awaitable[Any]:
        """Disable a bot.

        Parameters
        ----------
        bot_id : str
            Bot user ID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/{bot_id}/disable")

    def enable_bot(self, bot_id: str) -> Any | Awaitable[Any]:
        """Enable a bot.

        Parameters
        ----------
        bot_id : str
            Bot user ID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/{bot_id}/enable")

    def assign_bot_to_user(
        self, bot_id: str, user_id: str
    ) -> Any | Awaitable[Any]:
        """Assign a bot to a specified user.

        Parameters
        ----------
        bot_id : str
            Bot user ID.
        user_id : str
            The user ID to assign the bot to.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/{bot_id}/assign/{user_id}")

    def get_bot_lhs_icon(
        self, bot_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a bot's Left-Hand Sidebar icon image.

        Parameters
        ----------
        bot_id : str
            Bot user ID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{bot_id}/icon")

    def set_bot_lhs_icon(
        self, bot_id: str, image: str
    ) -> Any | Awaitable[Any]:
        """Set a bot's Left-Hand Sidebar icon image.

        Parameters
        ----------
        bot_id : str
            Bot user ID.
        image : str
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/{bot_id}/icon",
            files={"image": image},
        )

    def delete_bot_lhs_icon(self, bot_id: str) -> Any | Awaitable[Any]:
        """Delete a bot's Left-Hand Sidebar icon image.

        Parameters
        ----------
        bot_id : str
            Bot user ID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(f"{self.endpoint}/{bot_id}/icon")
