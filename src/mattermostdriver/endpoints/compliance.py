"""Class defining the /compliance API endpoint."""

from dataclasses import dataclass
from typing import Any, Awaitable, Dict

from requests import Response

from .base import APIEndpoint


@dataclass
class Compliance(APIEndpoint):
    """Class defining the /compliance API endpoint.

    Attributes
    ----------

    Methods
    -------

    """

    endpoint: str = "/compliance"

    def create_report(
        self, params: Dict[str, Any] | None
    ) -> Any | Awaitable[Any]:
        return self.client.post(f"{self.endpoint}/reports", params=params)

    def get_reports(
        self, params: Dict[str, Any] | None = None
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/reports", params=params)

    def get_report(
        self, report_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/reports/{report_id}")

    def download_report(
        self, report_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        return self.client.get(f"{self.endpoint}/reports/{report_id}/download")
