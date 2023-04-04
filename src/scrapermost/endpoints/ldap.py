"""Endpoints for configuring and interacting with LDAP."""

from dataclasses import dataclass
from typing import Any

from .base import APIEndpoint, _ret_json


@dataclass
class LDAP(APIEndpoint):
    """Class defining the LDAP API endpoint.

    Attributes
    ----------
    endpoint : str, default='ldap'
        The endpoint path.

    Methods
    -------
    sync_ldap()
        Sync with LDAP.
    test_ldap_config()
        Test LDAP configuration.

    """

    endpoint: str = "ldap"

    @_ret_json
    def sync_ldap(self) -> Any:
        """Sync with LDAP.

        Synchronize any user attribute changes in the configured AD/LDAP server
        with Mattermost.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/sync")

    @_ret_json
    def test_ldap_config(self) -> Any:
        """Test LDAP configuration.

        Test the current AD/LDAP configuration to see if the AD/LDAP server can
        be contacted successfully.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/test")
