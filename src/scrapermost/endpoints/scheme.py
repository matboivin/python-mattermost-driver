"""Endpoints for creating, getting and updating and deleting schemes."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict, Literal

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class Scheme(APIEndpoint):
    """Class defining the Schemes API endpoint.

    Attributes
    ----------
    endpoint : str, default='schemes'
        The endpoint path.

    Methods
    -------
    get_schemes(page=0, per_page=60, scope='')
        Get a page of schemes.
    create_scheme(body_json)
        Create a new scheme.
    get_scheme(scheme_id)
        Get a scheme from the provided scheme ID.
    delete_scheme(scheme_id)
        Mark the scheme as deleted in the database.
    patch_scheme(scheme_id, body_json)
        Update a scheme partially by providing only the fields to update.
    get_page_of_teams_using_scheme(scheme_id, page=0, per_page=60)
        Get a page of teams which use this scheme.
    get_page_of_channels_using_scheme(scheme_id, page=0, per_page=60)
        Get a page of channels which use this scheme.

    """

    endpoint: str = "schemes"

    @_ret_json
    def get_schemes(
        self,
        page: int = 0,
        per_page: int = 60,
        scope: Literal["", "team", "channel"] = "",
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of schemes.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).
        scope : '' or 'team' or 'channel', default=''
            Limit the results returned to the provided scope.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            self.endpoint,
            params={"scope": scope, "page": page, "per_page": per_page},
        )

    @_ret_json
    def create_scheme(self, body_json: Dict[str, Any]) -> Any:
        """Create a new scheme.

        Parameters
        ----------
        body_json : dict, optional
            The scheme settings as a dict.
            Example:
            {
                "name": "string",
                "description": "string",
                "scope": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(self.endpoint, body_json=body_json)

    @_ret_json
    def get_scheme(
        self, scheme_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a scheme from the provided scheme ID.

        Parameters
        ----------
        scheme_id : str
            Scheme GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{scheme_id}")

    @_ret_json
    def delete_scheme(self, scheme_id: str) -> Any:
        """Mark the scheme as deleted in the database.

        Parameters
        ----------
        scheme_id : str
            Scheme GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.delete(f"{self.endpoint}/{scheme_id}")

    @_ret_json
    def patch_scheme(self, scheme_id: str, body_json: Dict[str, Any]) -> Any:
        """Update a scheme partially by providing only the fields to update.

        Parameters
        ----------
        scheme_id : str
            Scheme GUID.
        body_json : dict, optional
            The scheme settings as a dict.
            Example:
            {
                "name": "string",
                "description": "string"
            }

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.put(
            f"{self.endpoint}/{scheme_id}/patch", body_json=body_json
        )

    @_ret_json
    def get_page_of_teams_using_scheme(
        self, scheme_id: str, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of teams which use this scheme.

        Parameters
        ----------
        scheme_id : str
            Scheme GUID.
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
            f"{self.endpoint}/{scheme_id}/teams",
            params={"page": page, "per_page": per_page},
        )

    @_ret_json
    def get_page_of_channels_using_scheme(
        self, scheme_id: str, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a page of channels which use this scheme.

        Parameters
        ----------
        scheme_id : str
            Scheme GUID.
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
            f"{self.endpoint}/{scheme_id}/channels",
            params={"page": page, "per_page": per_page},
        )
