"""Endpoints for creating, getting and updating webhooks."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class Webhooks(APIEndpoint):
    """Class defining the /hooks API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    create_incoming_hook(body_json)
        Create an incoming webhook for a channel.
    list_incoming_hooks(page=0, per_page=60, team_id=None)
        Get a page of a list of incoming webhooks.
    get_incoming_hook(hook_id)
        Get an incoming webhook given the hook ID.
    update_incoming_hook(hook_id, body_json)
        Update an incoming webhook given the hook ID.
    create_outgoing_hook(body_json)
        Create an outgoing webhook for a team.
    list_outgoing_hooks(page=0, per_page=60, team_id=None, channel_id=None)
        Get a page of a list of outgoing webhooks.
    get_outgoing_hook(hook_id)
        Get an outgoing webhook given the hook ID.
    delete_outgoing_hook(hook_id)
        Delete an outgoing webhook given the hook ID.
    update_outgoing_hook(hook_id, body_json)
        Update an outgoing webhook given the hook ID.
    regenerate_token_outgoing_hook(hook_id)
        Regenerate the token for the outgoing webhook.
    call_webhook(hook_id)
        Call a webhook.

    """

    endpoint: str = "/hooks"

    @_ret_json
    def create_incoming_hook(
        self, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Create an incoming webhook for a channel.

        Parameters
        ----------
        body_json : dict
            The webhook settings as a dict.
            {
                "channel_id": "string",
                "user_id": "string",
                "display_name": "string",
                "description": "string",
                "username": "string",
                "icon_url": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/incoming", body_json=body_json
        )

    @_ret_json
    def list_incoming_hooks(
        self, page: int = 0, per_page: int = 60, team_id: str | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of a list of incoming webhooks.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).
        team_id : str, optional
            Team GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        options: Any = {"page": page, "per_page": per_page}

        if team_id:
            options["team_id"] = team_id

        return self.client.get(f"{self.endpoint}/incoming", params=options)

    @_ret_json
    def get_incoming_hook(
        self, hook_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get an incoming webhook given the hook ID.

        Parameters
        ----------
        hook_id : str
            Incoming Webhook GUID

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/incoming/{hook_id}")

    @_ret_json
    def update_incoming_hook(
        self, hook_id: str, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update an incoming webhook given the hook ID.

        Parameters
        ----------
        hook_id : str
            Incoming Webhook GUID
        body_json : dict
            The hook settings as a dict.
            Example:
            {
                "id": "string",
                "channel_id": "string",
                "display_name": "string",
                "description": "string",
                "username": "string",
                "icon_url": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/incoming/{hook_id}", body_json=body_json
        )

    @_ret_json
    def create_outgoing_hook(
        self, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Create an outgoing webhook for a team.

        Parameters
        ----------
        body_json : dict
            The hook settings as a dict.
            Example:
            {
                "team_id": "string",
                "channel_id": "string",
                "creator_id": "string",
                "description": "string",
                "display_name": "string",
                "trigger_words": [
                    "string"
                ],
                "trigger_when": 0,
                "callback_urls": [
                    "string"
                ],
                "content_type": "application/x-www-form-urlencoded"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/outgoing", body_json=body_json
        )

    @_ret_json
    def list_outgoing_hooks(
        self,
        page: int = 0,
        per_page: int = 60,
        team_id: str | None = None,
        channel_id: str | None = None,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of a list of incoming webhooks.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).
        team_id : str, optional
            Team GUID.
        channel_id : str, optional
            channel_id GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        options: Any = {"page": page, "per_page": per_page}

        if team_id:
            options["team_id"] = team_id
        if channel_id:
            options["channel_id"] = channel_id

        return self.client.get(f"{self.endpoint}/outgoing", params=options)

    @_ret_json
    def get_outgoing_hook(
        self, hook_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get an outgoing webhook given the hook ID.

        Parameters
        ----------
        hook_id : str
            Incoming Webhook GUID

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/outgoing/{hook_id}")

    @_ret_json
    def delete_outgoing_hook(
        self, hook_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Delete an outgoing webhook given the hook ID.

        Parameters
        ----------
        hook_id : str
            Incoming Webhook GUID

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete(f"{self.endpoint}/outgoing/{hook_id}")

    @_ret_json
    def update_outgoing_hook(
        self, hook_id: str, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update an outgoing webhook given the hook ID.

        Parameters
        ----------
        hook_id : str
            Incoming Webhook GUID
        body_json : dict
            The hook settings as a dict.
            Example:
            {
                "id": "string",
                "channel_id": "string",
                "display_name": "string",
                "description": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/outgoing/{hook_id}", body_json=body_json
        )

    @_ret_json
    def regenerate_token_outgoing_hook(
        self, hook_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Regenerate the token for the outgoing webhook.

        Parameters
        ----------
        hook_id : str
            Incoming Webhook GUID

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/outgoing/{hook_id}/regen_token"
        )

    def call_webhook(
        self, hook_id: str, body_json: dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        """Call a webhook.

        Parameters
        ----------
        hook_id : str
            Incoming Webhook GUID
        body_json : dict, optional
            Parameters as a dict.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{hook_id}", body_json=body_json)
