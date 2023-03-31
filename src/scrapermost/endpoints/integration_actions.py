"""Endpoints for interactive actions for use by integrations."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from .base import APIEndpoint


@dataclass
class IntegrationActions(APIEndpoint):
    """Class defining the /actions API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    open_dialog(body_json)
        Open an interactive dialog.
    submit_dialog(body_json)
        Submit a dialog.

    """

    endpoint: str = "/actions"

    def open_dialog(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        """Open an interactive dialog.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/dialogs/open", body_json=body_json
        )

    def submit_dialog(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        """Submit a dialog.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/dialogs/submit", body_json=body_json
        )
