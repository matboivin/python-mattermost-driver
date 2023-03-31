"""Endpoints for getting and updating user statuses."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .users import Users


@dataclass
class Status(APIEndpoint):
    """Class defining the user status API endpoint.

    Note the endpoint is /user and not /status.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    get_user_status(user_id)
        Get user status by ID from the server.
    update_user_status(user_id, body_json=None)
        Manually set a user's status.
    get_user_statuses_by_id(body_json=None)
        Get a list of user statuses by ID from the server.

    """

    endpoint: str = Users.endpoint

    def get_user_status(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get user status by ID from the server.

        Parameters
        ----------
        user_id : str
            User GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{user_id}/status")

    def update_user_status(
        self, user_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        """Manually set a user's status.

        Parameters
        ----------
        user_id : str
            User GUID.
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{user_id}/status", body_json=body_json
        )

    def get_user_statuses_by_id(
        self, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        """Get a list of user statuses by ID from the server.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/status/ids", body_json)
