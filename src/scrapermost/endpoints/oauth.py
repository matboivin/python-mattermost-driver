"""Endpoints to configure and interact as an OAuth 2.0 service provider."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .users import Users


@dataclass
class OAuth(APIEndpoint):
    """Class defining the /oauth API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/oauth"

    def register_oauth_app(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/apps", body_json=body_json)

    def get_oauth_apps(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/apps", params=params)

    def get_oauth_app(
        self, app_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/apps/{app_id}")

    def delete_oauth_app(self, app_id: str) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/apps/" + app_id)

    def regenerate_oauth_app_secret(self, app_id: str) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/apps/{app_id}/regen_secret")

    def get_info_on_oauth_app(
        self, app_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/apps/{app_id}/info")

    def get_authorized_oauth_apps(
        self, user_id: str, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(
            f"{Users.endpoint}/{user_id}/oauth/apps/authorized", params=params
        )
