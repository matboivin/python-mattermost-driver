"""Class defining the /schemes API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Scheme(APIEndpoint):
    """Class defining the /schemes API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/schemes"

    def get_schemes(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(self.endpoint, params=params)

    def create_scheme(
        self, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, options=options)

    def get_scheme(
        self, scheme_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{scheme_id}")

    def delete_scheme(self, scheme_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/{scheme_id}")

    def patch_scheme(
        self, scheme_id: str, options: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{scheme_id}/patch", options=options
        )

    def get_page_of_teams_using_scheme(
        self, scheme_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{scheme_id}/teams", params=params
        )

    def get_page_of_channels_using_scheme(
        self, scheme_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{self.endpoint}/{scheme_id}/channels", params=params
        )
