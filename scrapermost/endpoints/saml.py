"""Endpoints for configuring and interacting with SAML."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint, _ret_json


@dataclass
class SAML(APIEndpoint):
    """Class defining the SAML API endpoint.

    Attributes
    ----------
    endpoint : str, default='saml'
        The endpoint path.

    Methods
    -------
    get_metadata()
        Get SAML metadata from the server.
    upload_idp_certificate(files)
        Upload IDP certificate.
    remove_idp_certificate()
        Delete the current IDP certificate being used.
    upload_public_certificate(files)
        Upload the public certificate to be used for encryption.
    remove_public_certificate()
        Delete the current public certificate being used.
    upload_private_key(files)
        Upload the private key to be used for encryption.
    remove_private_key()
        Delete the current private key being used.
    get_certificate_status()
        Get the status of the uploaded certificates and keys in use.

    """

    endpoint: str = "saml"

    @_ret_json
    def get_metadata(self) -> Any | Response | Awaitable[Any | Response]:
        """Get SAML metadata from the server.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/metadata")

    @_ret_json
    def upload_idp_certificate(
        self, files: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Upload IDP certificate.

        Parameters
        ----------
        files : dict
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/certificate/idp", files=files
        )

    @_ret_json
    def remove_idp_certificate(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Delete the current IDP certificate being used.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete(f"{self.endpoint}/certificate/idp")

    @_ret_json
    def upload_public_certificate(
        self, files: dict[str, Any] | None
    ) -> Any | Response | Awaitable[Any | Response]:
        """Upload the public certificate to be used for encryption.

        Parameters
        ----------
        files : dict
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/certificate/public", files=files
        )

    @_ret_json
    def remove_public_certificate(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Delete the current public certificate being used.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete(f"{self.endpoint}/certificate/public")

    @_ret_json
    def upload_private_key(
        self, files: dict[str, Any]
    ) -> Any | Response | Awaitable[Any | Response]:
        """Upload the private key to be used for encryption.

        Parameters
        ----------
        files : dict
            The image's bytes string to be uploaded.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(
            f"{self.endpoint}/certificate/private", files=files
        )

    @_ret_json
    def remove_private_key(self) -> Any | Response | Awaitable[Any | Response]:
        """Delete the current private key being used.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.delete(f"{self.endpoint}/certificate/private")

    @_ret_json
    def get_certificate_status(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get the status of the uploaded certificates and keys in use.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/certificate/status")
