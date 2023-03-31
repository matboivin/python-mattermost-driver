"""Endpoints for configuring and interacting with SAML."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class SAML(APIEndpoint):
    """Class defining the /saml API endpoint.

    Attributes
    ----------
    endpoint : str
        The endpoint path.

    Methods
    -------

    """

    endpoint: str = "/saml"

    def get_metadata(self) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/metadata")

    def upload_idp_certificate(
        self, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/certificate/idp", files=files
        )

    def remove_idp_certificate(self) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/certificate/idp")

    def upload_public_certificate(
        self, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/certificate/public", files=files
        )

    def remove_public_certificate(self) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/certificate/public")

    def upload_private_key(
        self, files: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(
            f"{self.endpoint}/certificate/private", files=files
        )

    def remove_private_key(self) -> Any | Awaitable[Any]:
        return self.client.delete(f"{self.endpoint}/certificate/private")

    def get_certificate_status(
        self,
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/certificate/status")
