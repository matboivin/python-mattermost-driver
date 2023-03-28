"""Class defining the /files API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Files(APIEndpoint):
    """Class defining the /files API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/files"

    def upload_file(
        self, channel_id: str, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            self.endpoint, data={"channel_id": channel_id}, files=files
        )

    def get_file(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{file_id}")

    def get_file_thumbnail(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{file_id}/thumbnail")

    def get_file_preview(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{file_id}/preview")

    def get_public_file_link(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{file_id}/link")

    def get_file_metadata(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/{file_id}/info")
