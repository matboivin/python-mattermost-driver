"""Endpoints for creating, getting and downloading compliance reports."""

from dataclasses import dataclass
from typing import Any, Awaitable

from requests import Response

from .base import APIEndpoint


@dataclass
class Compliance(APIEndpoint):
    """Class defining the Compliance API endpoint.

    Attributes
    ----------
    endpoint : str, default='compliance'
        The endpoint path.

    Methods
    -------
    create_report()
        Create and save a compliance report.
    get_reports(page=0, per_page=60)
        Get a list of compliance reports previously created by page.
    get_report(report_id)
        Get a compliance reports previously created.
    download_report(report_id)
        Download the full contents of a report as a file.

    """

    endpoint: str = "compliance"

    def create_report(self) -> Any | Awaitable[Any]:
        """Create and save a compliance report.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.post(f"{self.endpoint}/reports")

    def get_reports(
        self, page: int = 0, per_page: int = 60
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a list of compliance reports previously created by page.

        Parameters
        ----------
        page : int, default=0
            The page to select.
        per_page : int, default=60
            The number of members per page (max: 200).

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(
            f"{self.endpoint}/reports",
            params={"page": page, "per_page": per_page},
        )

    def get_report(
        self, report_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Get a compliance reports previously created.

        Parameters
        ----------
        report_id : str
            Compliance report GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/reports/{report_id}")

    def download_report(
        self, report_id: str
    ) -> Any | Response | Awaitable[Any | Response]:
        """Download the full contents of a report as a file.

        Parameters
        ----------
        report_id : str
            Compliance report GUID.

        Returns
        -------
        Any or Coroutine(...) -> Any
        or requests.Response or Coroutine(...) -> requests.Response

        """
        return self.client.get(f"{self.endpoint}/reports/{report_id}/download")
