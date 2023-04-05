"""Endpoints for configuring and interacting with Elasticsearch."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class Elasticsearch(APIEndpoint):
    """Class defining the ElasticSearch API endpoint.

    Attributes
    ----------
    endpoint : str, default='elasticsearch'
        The endpoint path.

    Methods
    -------
    test_elasticsearch_configuration()
        Test Elasticsearch configuration.
    purge_all_elasticsearch_indexes()
        Purge all Elasticsearch indexes.

    """

    endpoint: str = "elasticsearch"

    @_ret_json
    def test_elasticsearch_configuration(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Test Elasticsearch configuration.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/test")

    @_ret_json
    def purge_all_elasticsearch_indexes(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Purge all Elasticsearch indexes.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/purge_indexes")
