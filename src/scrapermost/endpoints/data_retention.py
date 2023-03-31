"""Endpoint for getting data retention policy settings."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint


@dataclass
class DataRetention(APIEndpoint):
    """Class defining the /data_retention API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    get_data_retention_policy()
        Get the policies which are applied to a user's teams.

    """

    endpoint: str = "/data_retention"

    def get_data_retention_policy(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get the policies which are applied to a user's teams.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/policy")
