"""Class defining the /cluster API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint


@dataclass
class Cluster(APIEndpoint):
    """Class defining the /cluster API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/cluster"

    def get_cluster_status(self) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/status")
