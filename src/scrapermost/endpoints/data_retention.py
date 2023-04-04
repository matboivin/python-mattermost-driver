"""Endpoint for getting data retention policy settings."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class DataRetention(APIEndpoint):
    """Class defining the Data retention policy API endpoint.

    Attributes
    ----------
    endpoint : str, default='data_retention'
        The endpoint path.

    Methods
    -------
    get_data_retention_policy()
        Get the policies which are applied to a user's teams.

    """

    endpoint: str = "data_retention"

    @_ret_json
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
