"""Endpoints for configuring and interacting with LDAP."""

from dataclasses import dataclass
from typing import Any, Awaitable

from .base import APIEndpoint


@dataclass
class LDAP(APIEndpoint):
    """Class defining the /ldap API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    sync_ldap()
        Sync with LDAP.
    test_ldap_config()
        Test LDAP configuration.

    """

    endpoint: str = "/ldap"

    def sync_ldap(self) -> Any | Awaitable[Any]:
        """Sync with LDAP.

        Synchronize any user attribute changes in the configured AD/LDAP server
        with Mattermost.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/sync")

    def test_ldap_config(self) -> Any | Awaitable[Any]:
        """Test LDAP configuration.

        Test the current AD/LDAP configuration to see if the AD/LDAP server can
        be contacted successfully.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/test")
