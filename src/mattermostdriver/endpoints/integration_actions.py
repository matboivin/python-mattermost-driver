"""Class defining the /actions API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from .base import APIEndpoint


@dataclass
class IntegrationActions(APIEndpoint):
    """Class defining the /actions API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/actions"

    def open_dialog(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/dialogs/open", options=options
        )

    def submit_dialog(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/dialogs/submit", options=options
        )
