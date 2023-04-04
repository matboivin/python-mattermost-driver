"""Endpoints related to custom branding and white-labeling."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


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

    @_ret_json
    def get_brand_image(self) -> Any | Response | Awaitable[Any | Response]:
        """Get the previously uploaded brand image.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/image")

    @_ret_json
    def upload_brand_image(self, image: str) -> Any:
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
