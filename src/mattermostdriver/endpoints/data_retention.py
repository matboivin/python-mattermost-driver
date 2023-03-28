"""Class defining the /data_retention API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint


@dataclass
class DataRetention(APIEndpoint):
    """Class defining the /data_retention API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/data_retention"

    def get_data_retention_policy(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/policy")
