"""Generic base class for API endpoints."""

from dataclasses import dataclass

from scrapermost.driver import AsyncClient, Client


@dataclass
class APIEndpoint:
    """Base class defining an API endpoint.

    Attributes
    ----------
    client : driver.async_client.AsyncClient or driver.client.Client
        The underlying client object.

    """

    client: AsyncClient | Client
