"""Class defining the /ldap API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable

from .base import APIEndpoint


@dataclass
class LDAP(APIEndpoint):
    """Class defining the /ldap API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/ldap"

    def sync_ldap(self) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/sync")

    def test_ldap_config(self) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/test")
