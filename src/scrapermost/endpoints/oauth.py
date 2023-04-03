"""Endpoints to configure and interact as an OAuth 2.0 service provider."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint
from .users import Users


@dataclass
class OAuth(APIEndpoint):
    """Class defining the OAuth API endpoint.

    Attributes
    ----------
    endpoint : str, default='oauth'
        The endpoint path.

    Methods
    -------
    register_oauth_app(body_json)
        Register an OAuth 2.0 client application.
    get_oauth_apps(page=0, per_page=60)
        Get a page of OAuth 2.0 client applications.
    get_oauth_app(app_id)
        Get an OAuth 2.0 client application.
    delete_oauth_app(app_id)
        Delete and unregister an OAuth 2.0 client application.
    regenerate_oauth_app_secret(app_id)
        Regenerate the client secret for an OAuth 2.0 client app.
    get_info_on_oauth_app(app_id)
        Get public information about an OAuth 2.0 client application.
    get_authorized_oauth_apps(user_id, page=0, per_page=60)
        Get a page of OAuth 2.0 client apps that can access user accounts.

    """

    endpoint: str = "oauth"

    def register_oauth_app(
        self, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Register an OAuth 2.0 client application.

        Parameters
        ----------
        body_json : dict
            The OAuth application settings as a dict.
            Example:
            {
                "name": "string",
                "description": "string",
                "icon_url": "string",
                "callback_urls": [
                    "string"
                ],
                "homepage": "string",
                "is_trusted": true
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/apps", body_json=body_json)

    def get_oauth_apps(
        self, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of OAuth 2.0 client applications.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/apps",
            params={"page": page, "per_page": per_page},
        )

    def get_oauth_app(
        self, app_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get an OAuth 2.0 client application.

        Parameters
        ----------
        app_id : str
            Application client ID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/apps/{app_id}")

    def delete_oauth_app(self, app_id: str) -> Any | Awaitable[Any]:
        """Delete and unregister an OAuth 2.0 client application.

        Parameters
        ----------
        app_id : str
            Application client ID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(f"{self.endpoint}/apps/{app_id}")

    def regenerate_oauth_app_secret(self, app_id: str) -> Any | Awaitable[Any]:
        """Regenerate the client secret for an OAuth 2.0 client app.

        Parameters
        ----------
        app_id : str
            Application client ID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/apps/{app_id}/regen_secret")

    def get_info_on_oauth_app(
        self, app_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get public information about an OAuth 2.0 client application.

        Parameters
        ----------
        app_id : str
            Application client ID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/apps/{app_id}/info")

    def get_authorized_oauth_apps(
        self, user_id: str, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of OAuth 2.0 client apps that can access user accounts.

        Parameters
        ----------
        user_id : str
            User GUID.
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{Users.endpoint}/{user_id}/{self.endpoint}/apps/authorized",
            params={"page": page, "per_page": per_page},
        )
