"""Endpoints related to custom branding and white-labeling."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint


@dataclass
class Brand(APIEndpoint):
    """Class defining the Brand API endpoint.

    Attributes
    ----------
    endpoint : str, default='brand'
        The endpoint path.

    Methods
    -------
    get_brand_image()
        Get the previously uploaded brand image.
    upload_brand_image(image)
        Upload a brand image.

    """

    endpoint: str = "brand"

    def get_brand_image(self) -> Any | Response | Awaitable[Any | Response]:
        """Get the previously uploaded brand image.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/image")

    def upload_brand_image(self, image: str) -> Any | Awaitable[Any]:
        """Upload a brand image.

        Parameters
        ----------
        image : str
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            f"{self.endpoint}/image", files={"image": image}
        )
