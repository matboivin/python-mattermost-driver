"""Endpoints for creating, getting and updating roles."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class Roles(APIEndpoint):
    """Class defining the Roles API endpoint.

    Attributes
    ----------
    endpoint : str, default='roles'
        The endpoint path.

    Methods
    -------
    get_role_by_id(role_id)
        Get a role from the provided role ID.
    get_role_by_name(role_name)
        Get a role from the provided role name.
    patch_role(role_id, body_json)
        Update a role partially by providing only the fields to update.
    get_list_of_roles_by_name()
        Get a list of roles from their names.

    """

    endpoint: str = "roles"

    @_ret_json
    def get_role_by_id(
        self, role_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a role from the provided role ID.

        Parameters
        ----------
        role_id : str
            Role GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{role_id}")

    @_ret_json
    def get_role_by_name(
        self, role_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a role from the provided role ID.

        Parameters
        ----------
        role_name : str
            Role name.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/name/{role_name}")

    @_ret_json
    def patch_role(
        self, role_id: str, body_json: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Update a role partially by providing only the fields to update.

        Parameters
        ----------
        role_id : str
            Role GUID.
        body_json : dict
            The role settings as a dict.
            Example:
            {
                "permissions": [
                    "string"
                ]
            }

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.put(
            f"{self.endpoint}/{role_id}/patch", body_json=body_json
        )

    @_ret_json
    def get_list_of_roles_by_name(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of roles from their names.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/names")
