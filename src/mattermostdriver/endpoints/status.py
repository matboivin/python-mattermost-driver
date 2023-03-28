"""Class defining the user status API endpoint."""

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

    Methods
    -------

    """

    endpoint: str = Users.endpoint

    def get_user_status(
        self, user_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{user_id}/status")

    def update_user_status(
        self, user_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{user_id}/status", options=options
        )

    def get_user_statuses_by_id(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/status/ids", options)
