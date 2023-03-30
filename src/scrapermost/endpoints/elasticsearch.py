"""Class defining the /elasticsearch API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable

from .base import APIEndpoint


@dataclass
class Elasticsearch(APIEndpoint):
    """Class defining the /elasticsearch API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/elasticsearch"

    def test_elasticsearch_configuration(self) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/test")

    def purge_all_elasticsearch_indexes(self) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/purge_indexes")
