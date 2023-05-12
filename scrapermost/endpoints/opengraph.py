"""Endpoint for getting Open Graph metadata."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class Opengraph(APIEndpoint):
    """Class defining the OpenGraph API endpoint.

    Attributes
    ----------
    endpoint : str, default='opengraph'
        The endpoint path.

    Methods
    -------
    get_opengraph_metadata_for_url(body_json)
        Get Open Graph Metadata for a specif URL.

    """

    endpoint: str = "opengraph"

    @_ret_json
    def get_opengraph_metadata_for_url(
        self, body_json: dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get Open Graph Metadata for a specif URL.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(self.endpoint, body_json=body_json)
