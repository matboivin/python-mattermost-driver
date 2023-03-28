"""Class defining the /opengraph API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from .base import APIEndpoint


@dataclass
class Opengraph(APIEndpoint):
    """Class defining the /opengraph API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/opengraph"

    def get_opengraph_metadata_for_url(
        self, options: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(self.endpoint, options=options)
