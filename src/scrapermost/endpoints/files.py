"""Endpoints for uploading and interacting with files."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Files(APIEndpoint):
    """Class defining the /files API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------
    upload_file(channel_id, files)
        Uploads a file that can later be attached to a post.
    get_file(file_id)
        Gets a file that has been uploaded previously.
    get_file_thumbnail(file_id)
        Gets a file's thumbnail.
    get_file_preview(file_id)
        Gets a file's preview.
    get_public_file_link(file_id)
        Get a public file link.
    get_file_metadata(file_id)
        Gets a file's info.

    """

    endpoint: str = "/files"

    def upload_file(
        self, channel_id: str, files: Dict[str, Any]
    ) -> Any | Awaitable[Any]:
        """Uploads a file that can later be attached to a post.

        Parameters
        ----------
        channel_id : str
            Channel GUID.
        files : dict
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any

        """
        return self.client.post(
            self.endpoint, data={"channel_id": channel_id}, files=files
        )

    def get_file(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Gets a file that has been uploaded previously.

        Parameters
        ----------
        file_id : str
            File GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{file_id}")

    def get_file_thumbnail(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Gets a file's thumbnail.

        Parameters
        ----------
        file_id : str
            File GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{file_id}/thumbnail")

    def get_file_preview(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Gets a file's preview.

        Parameters
        ----------
        file_id : str
            File GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{file_id}/preview")

    def get_public_file_link(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a public file link.

        Gets a public link for a file that can be accessed without logging
        into Mattermost.

        Parameters
        ----------
        file_id : str
            File GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{file_id}/link")

    def get_file_metadata(
        self, file_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Gets a file's info.

        Parameters
        ----------
        file_id : str
            File GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/{file_id}/info")