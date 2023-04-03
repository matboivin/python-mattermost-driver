"""Endpoints for creating, getting and updating roles."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


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
        Partially update a role by providing only the fields to update.
    get_list_of_roles_by_name()
        Get a list of roles from their names.

    """

    endpoint: str = "roles"

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

    def get_role_by_name(
        self, role_name: str
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
        return self.client.get(f"{self.endpoint}/name/{role_name}")

    def patch_role(
        self, role_id: str, body_json: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Partially update a role by providing only the fields to update.

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

        """
        return self.client.put(
            f"{self.endpoint}/{role_id}/patch", body_json=body_json
        )

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
