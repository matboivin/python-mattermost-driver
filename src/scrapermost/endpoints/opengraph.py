"""Endpoint for getting Open Graph metadata."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from .base import APIEndpoint


@dataclass
class Opengraph(APIEndpoint):
    """Class defining the /opengraph API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    get_opengraph_metadata_for_url(body_json)
        Get Open Graph Metadata for a specif URL.

    """

    endpoint: str = "/opengraph"

    def get_opengraph_metadata_for_url(
        self, body_json: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        """Get Open Graph Metadata for a specif URL.

        Parameters
        ----------
        body_json : dict, optional
            A JSON serializable object to include in the body of the request.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(self.endpoint, body_json=body_json)
