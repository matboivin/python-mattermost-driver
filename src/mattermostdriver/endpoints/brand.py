"""Class defining the /brand API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Brand(APIEndpoint):
    """Class defining the /brand API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/brand"

    def get_brand_image(self) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/image")

    def upload_brand_image(
        self, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/image", files=files)
