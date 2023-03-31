"""Endpoints for creating, getting and updating roles."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Roles(APIEndpoint):
    """Class defining the /roles API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/roles"

    def get_role_by_id(
        self, role_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{role_id}")

    def get_role_by_name(
        self, role_name: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/name/{role_name}")

    def patch_role(
        self, role_id: str, body_json: Dict[str, Any] | None = None
    ) -> Any | Awaitable[Any]:
        return self.client.put(
            f"{self.endpoint}/{role_id}/patch", body_json=body_json
        )

    def get_list_of_roles_by_name(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/names")
