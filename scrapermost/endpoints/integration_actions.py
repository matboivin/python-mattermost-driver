"""Endpoints for interactive actions for use by integrations."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class IntegrationActions(APIEndpoint):
    """Class defining the integrations actions API endpoint.

    Attributes
    ----------
    endpoint : str, default='actions'
        The endpoint path.

    Methods
    -------
    open_dialog(body_json)
        Open an interactive dialog.
    submit_dialog(body_json)
        Submit a dialog.

    """

    endpoint: str = "actions"

    @_ret_json
    def open_dialog(
        self, body_json: dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Open an interactive dialog.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/dialogs/open", body_json=body_json
        )

    @_ret_json
    def submit_dialog(
        self, body_json: dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Submit a dialog.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/dialogs/submit", body_json=body_json
        )
