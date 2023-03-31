"""Endpoints for configuring and interacting with Elasticsearch."""

from dataclasses import dataclass
from typing import Any, Awaitable

from .base import APIEndpoint


@dataclass
class Elasticsearch(APIEndpoint):
    """Class defining the /elasticsearch API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    test_elasticsearch_configuration()
        Test Elasticsearch configuration.
    purge_all_elasticsearch_indexes()
        Purge all Elasticsearch indexes.

    """

    endpoint: str = "/elasticsearch"

    def test_elasticsearch_configuration(self) -> Any | Awaitable[Any]:
        """Test Elasticsearch configuration.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/test")

    def purge_all_elasticsearch_indexes(self) -> Any | Awaitable[Any]:
        """Purge all Elasticsearch indexes.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(f"{self.endpoint}/purge_indexes")
